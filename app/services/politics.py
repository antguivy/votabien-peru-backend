# app/services/politics.py

from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import aliased, joinedload, selectinload
from sqlmodel import Session, or_, select

from app.models.politics import (
    Candidato,
    Distrito,
    EstadoCandidatura,
    Legislador,
    PartidoPolitico,
    Persona,
    ProcesoElectoral,
    ProyectoLey,
    TipoCamara,
    TipoCandidatura,
)
from app.schemas.politics import (
    CreateCandidaturaRequest,
    CreateLegisladorPeriodoRequest,
    CreatePartidoRequest,
    CreatePersonaRequest,
    CreateProcesoElectoralRequest,
    UpdatePersonaRequest,
)

# ==============================================================================
# == SERVICIOS PARA PERSONA
# ==============================================================================


async def get_personas_list(
    session: Session,
    es_legislador_activo: bool,
    camara: Optional[TipoCamara],
    partidos: Optional[List[str]],
    distritos: Optional[List[str]],
    search: Optional[str],
    skip: int,
    limit: int,
):
    query = select(Persona).options(
        selectinload(Persona.periodos_legislativos).selectinload(Legislador.partido),
        selectinload(Persona.periodos_legislativos).selectinload(Legislador.distrito),
    )

    if es_legislador_activo:
        # alias para evitar conflictos
        legislador_alias = aliased(Legislador)

        query = query.join(
            legislador_alias, Persona.id == legislador_alias.persona_id
        ).where(legislador_alias.esta_activo)

        if camara:
            query = query.where(legislador_alias.camara == camara)

        if partidos:
            partido_alias = aliased(PartidoPolitico)
            query = query.join(
                partido_alias, legislador_alias.partido_id == partido_alias.id
            ).where(partido_alias.nombre.in_(partidos))

        if distritos:
            distrito_alias = aliased(Distrito)
            query = query.join(
                distrito_alias, legislador_alias.distrito_id == distrito_alias.id
            ).where(distrito_alias.nombre.in_(distritos))

    if search:
        search_term = f"%{search.lower()}%"
        query = query.where(
            or_(
                Persona.nombre_completo.ilike(search_term),
                Persona.dni.ilike(search_term),
                Persona.nombres.ilike(search_term),
                Persona.apellidos.ilike(search_term),
            )
        )

    query = query.distinct(Persona.id).offset(skip).limit(limit)

    personas = session.exec(query).all()

    return [
        {
            **persona.model_dump(),
            "periodo_activo": next(
                (p for p in persona.periodos_legislativos if p.esta_activo), None
            ),
        }
        for persona in personas
    ]


async def get_persona_by_id(persona_id: str, session: Session):
    """Obtener una persona por su ID con todo su historial político."""
    query = (
        select(Persona)
        .where(Persona.id == persona_id)
        .options(
            selectinload(Persona.periodos_legislativos).selectinload(
                Legislador.partido
            ),
            selectinload(Persona.periodos_legislativos).selectinload(
                Legislador.distrito
            ),
            selectinload(Persona.periodos_legislativos).selectinload(
                Legislador.proyectos_ley
            ),
            selectinload(Persona.candidaturas).selectinload(
                Candidato.proceso_electoral
            ),
            selectinload(Persona.candidaturas).selectinload(Candidato.partido),
            selectinload(Persona.candidaturas).selectinload(Candidato.distrito),
        )
    )
    persona = session.exec(query).first()
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona no encontrada"
        )
    return persona


async def create_persona(data: CreatePersonaRequest, session: Session):
    """Crear una nueva Persona en la base de datos."""
    existing = session.exec(select(Persona).where(Persona.dni == data.dni)).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una persona con el DNI {data.dni}",
        )

    nombre_completo = f"{data.nombres} {data.apellidos}".strip()

    persona = Persona.model_validate(data, update={"nombre_completo": nombre_completo})

    session.add(persona)
    session.commit()
    session.refresh(persona)
    return persona


async def update_persona(persona_id: str, data: UpdatePersonaRequest, session: Session):
    """Actualizar los datos biográficos de una Persona."""
    persona = session.get(Persona, persona_id)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona no encontrada"
        )

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(persona, key, value)

    if "nombres" in update_data or "apellidos" in update_data:
        persona.nombre_completo = f"{persona.nombres} {persona.apellidos}".strip()

    session.add(persona)
    session.commit()
    session.refresh(persona)
    return persona


async def get_proyectos_by_persona(
    persona_id: str, session: Session, skip: int, limit: int
):
    """
    Obtener todos los proyectos de ley de una persona
    a lo largo de todos sus periodos legislativos.
    """
    query = (
        select(ProyectoLey)
        .join(Legislador)
        .where(Legislador.persona_id == persona_id)
        .order_by(ProyectoLey.fecha_presentacion.desc())
        .offset(skip)
        .limit(limit)
    )
    return session.exec(query).all()


# ==============================================================================
# == SERVICIOS PARA ROLES (LEGISLADOR Y CANDIDATO)
# ==============================================================================


async def add_legislador_periodo(
    data: CreateLegisladorPeriodoRequest, session: Session
):
    """Añadir un nuevo rol/periodo legislativo a una Persona existente."""
    persona = session.get(Persona, data.persona_id)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona no encontrada para asignar el rol",
        )
    if not session.get(PartidoPolitico, data.partido_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partido político no encontrado",
        )

    if not session.get(Distrito, data.distrito_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Distrito no encontrado",
        )

    periodo = Legislador.model_validate(data)
    session.add(periodo)
    session.commit()
    session.refresh(periodo)
    return periodo


# ==============================================================================
# == SERVICIOS PARA CANDIDATURAS
# ==============================================================================


async def get_candidaturas_list(
    session: Session,
    proceso_electoral_id: Optional[str],
    tipo: Optional[TipoCandidatura],
    partidos: Optional[List[str]],
    distritos: Optional[List[str]],
    estado: Optional[EstadoCandidatura],
    search: Optional[str],
    skip: int = 0,
    limit: int = 20,
):
    """
    Obtiene candidaturas con persona, partido, distrito, proceso_electoral y periodos_legislativos.
    Aplana los periodos_legislativos al nivel superior.
    Totalmente optimizado.
    """

    filters = []
    if proceso_electoral_id:
        filters.append(Candidato.proceso_electoral_id == proceso_electoral_id)
    if tipo:
        filters.append(Candidato.tipo == tipo)
    if estado:
        filters.append(Candidato.estado == estado)

    query = (
        select(Candidato)
        .where(*filters)
        .options(
            selectinload(Candidato.partido),
            selectinload(Candidato.distrito),
            selectinload(Candidato.proceso_electoral),
            selectinload(Candidato.persona)
            .selectinload(Persona.periodos_legislativos)
            .options(
                joinedload(Legislador.partido),
                joinedload(Legislador.distrito),
                joinedload(Legislador.proyectos_ley),
            ),
        )
        .order_by(Candidato.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    if partidos:
        query = query.join(Candidato.partido).where(
            PartidoPolitico.nombre.in_(partidos)
        )
    if distritos:
        query = query.join(Candidato.distrito).where(Distrito.nombre.in_(distritos))
    if search:
        s = f"%{search.lower()}%"
        query = query.join(Candidato.persona).where(
            or_(
                Persona.nombre_completo.ilike(s),
                Persona.nombres.ilike(s),
                Persona.apellidos.ilike(s),
            )
        )

    candidatos = session.exec(query).unique().all()

    resultado = []
    for c in candidatos:
        persona = c.persona

        candidatura_dict = c.model_dump()
        candidatura_dict.update(
            {
                "persona": persona.model_dump() if persona else None,
                "periodos_legislativos": [
                    {
                        **p.model_dump(),
                        "partido": p.partido.model_dump() if p.partido else None,
                        "distrito": p.distrito.model_dump() if p.distrito else None,
                        "proyectos_ley": [pl.model_dump() for pl in p.proyectos_ley]
                        if hasattr(p, "proyectos_ley")
                        else [],
                    }
                    for p in (persona.periodos_legislativos if persona else [])
                ],
                "partido": c.partido.model_dump() if c.partido else None,
                "distrito": c.distrito.model_dump() if c.distrito else None,
                "proceso_electoral": c.proceso_electoral.model_dump()
                if c.proceso_electoral
                else None,
            }
        )

        resultado.append(candidatura_dict)

    return resultado


async def get_candidatura_by_id(candidatura_id: str, session: Session):
    """Obtener una candidatura específica con todos sus detalles."""
    query = (
        select(Candidato)
        .where(Candidato.id == candidatura_id)
        .options(
            selectinload(Candidato.persona),
            selectinload(Candidato.partido),
            selectinload(Candidato.distrito),
            selectinload(Candidato.proceso_electoral),
        )
    )
    candidatura = session.exec(query).first()
    if not candidatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidatura no encontrada"
        )
    return candidatura


async def add_candidatura(data: CreateCandidaturaRequest, session: Session):
    """Añadir una nueva candidatura a una Persona."""
    if not session.get(Persona, data.persona_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona no encontrada para la candidatura",
        )

    if not session.get(ProcesoElectoral, data.proceso_electoral_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proceso electoral no encontrado",
        )

    if not session.get(PartidoPolitico, data.partido_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partido político no encontrado",
        )

    if data.distrito_id and not session.get(Distrito, data.distrito_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Distrito no encontrado",
        )

    candidatura = Candidato.model_validate(data)
    session.add(candidatura)
    session.commit()
    session.refresh(candidatura)

    return await get_candidatura_by_id(candidatura.id, session)


async def update_candidatura(
    candidatura_id: str, data: CreateCandidaturaRequest, session: Session
):
    """Actualizar una candidatura existente."""
    candidatura = session.get(Candidato, candidatura_id)
    if not candidatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidatura no encontrada"
        )

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(candidatura, key, value)

    session.add(candidatura)
    session.commit()
    session.refresh(candidatura)
    return await get_candidatura_by_id(candidatura_id, session)


# ==============================================================================
# == SERVICIOS PARA PROCESOS ELECTORALES
# ==============================================================================


async def get_procesos_electorales(session: Session, activo: Optional[bool]):
    """Obtener lista de procesos electorales."""
    query = select(ProcesoElectoral).order_by(ProcesoElectoral.año.desc())

    if activo is not None:
        query = query.where(ProcesoElectoral.activo == activo)

    return session.exec(query).all()


async def get_proceso_electoral_by_id(proceso_id: str, session: Session):
    """Obtener un proceso electoral específico."""
    proceso = session.get(ProcesoElectoral, proceso_id)
    if not proceso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proceso electoral no encontrado",
        )
    return proceso


async def create_proceso_electoral(
    data: CreateProcesoElectoralRequest, session: Session
):
    """Crear un nuevo proceso electoral."""
    existing = session.exec(
        select(ProcesoElectoral).where(ProcesoElectoral.año == data.año)
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un proceso electoral para el año {data.año}",
        )

    proceso = ProcesoElectoral.model_validate(data)
    session.add(proceso)
    session.commit()
    session.refresh(proceso)
    return proceso


# ==============================================================================
# == SERVICIOS PARA PARTIDOS POLÍTICOS
# ==============================================================================


async def get_partidos_list(session: Session, activo: Optional[bool]):
    """Obtener lista de partidos políticos."""
    query = select(PartidoPolitico).order_by(PartidoPolitico.nombre)

    if activo is not None:
        query = query.where(PartidoPolitico.activo == activo)

    return session.exec(query).all()


async def get_partido_by_id(partido_id: str, session: Session):
    """Obtener un partido político específico."""
    partido = session.get(PartidoPolitico, partido_id)
    if not partido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partido político no encontrado",
        )
    return partido


async def create_partido(data: CreatePartidoRequest, session: Session):
    """Crear un nuevo partido político."""
    existing_nombre = session.exec(
        select(PartidoPolitico).where(PartidoPolitico.nombre == data.nombre)
    ).first()

    if existing_nombre:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un partido con el nombre '{data.nombre}'",
        )

    existing_sigla = session.exec(
        select(PartidoPolitico).where(PartidoPolitico.sigla == data.sigla)
    ).first()

    if existing_sigla:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un partido con la sigla '{data.sigla}'",
        )

    partido = PartidoPolitico.model_validate(data)
    session.add(partido)
    session.commit()
    session.refresh(partido)
    return partido


# ==============================================================================
# == SERVICIOS PARA DISTRITOS
# ==============================================================================


async def get_distritos_list(session: Session):
    """Obtener lista de distritos electorales."""
    query = select(Distrito).where(Distrito.activo).order_by(Distrito.nombre)
    return session.exec(query).all()


async def get_distrito_by_id(distrito_id: str, session: Session):
    """Obtener un distrito específico."""
    distrito = session.get(Distrito, distrito_id)
    if not distrito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Distrito no encontrado"
        )
    return distrito
