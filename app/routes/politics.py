from typing import List, Optional

from app.config.database import get_session
from app.config.security import get_current_user, oauth2_scheme
from app.models.politics import EstadoCandidatura, TipoCamara, TipoCandidatura
from app.responses.politics import (
    CandidaturaDetailResponse,
    DistritoElectoralResponse,
    PartidoPoliticoDetailResponse,
    PartidoPoliticoResponse,
    PersonaDetailResponse,
    PersonaListResponse,
    ProcesoElectoralResponse,
    ProyectoLeyResponse,
)
from app.schemas.politics import (
    CreateCandidaturaRequest,
    CreateLegisladorPeriodoRequest,
    CreatePartidoRequest,
    CreatePersonaRequest,
    CreateProcesoElectoralRequest,
    UpdatePersonaRequest,
)
from app.services import politics
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

# ====== RUTAS PÚBLICAS ======
politics_public_router = APIRouter(
    prefix="/politics",
    tags=["Politics - Public"],
    responses={404: {"description": "Not found"}},
)

# ========== PERSONAS / LEGISLADORES ACTUALES ==========


@politics_public_router.get(
    "/personas",
    status_code=status.HTTP_200_OK,
    response_model=List[PersonaListResponse],
    summary="Listar personas políticas",
    description="Obtener lista de personas con roles políticos actuales o históricos",
)
async def get_personas_list(
    es_legislador_activo: bool = Query(False),
    camara: Optional[TipoCamara] = Query(None),
    partidos: Optional[List[str]] = Query(None),
    distritos: Optional[List[str]] = Query(None),
    search: Optional[str] = Query(None, description="Buscar por nombre completo o DNI"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session),
):
    """
    Endpoint principal para obtener legisladores actuales.
    Útil para mostrar el Congreso actual, o futuros Senado/Diputados.
    """
    return await politics.get_personas_list(
        session=session,
        es_legislador_activo=es_legislador_activo,
        camara=camara,
        partidos=partidos,
        distritos=distritos,
        search=search,
        skip=skip,
        limit=limit,
    )


@politics_public_router.get(
    "/personas/{persona_id}",
    status_code=status.HTTP_200_OK,
    response_model=PersonaDetailResponse,
    summary="Detalle completo de una persona política",
)
async def get_persona_detail(persona_id: str, session: Session = Depends(get_session)):
    """
    Obtiene toda la información de una persona:
    - Datos biográficos
    - Historial de periodos legislativos
    - Historial de candidaturas
    - Proyectos de ley
    """
    return await politics.get_persona_by_id(persona_id, session)


@politics_public_router.get(
    "/personas/{persona_id}/proyectos",
    status_code=status.HTTP_200_OK,
    response_model=List[ProyectoLeyResponse],
    summary="Proyectos de ley de una persona",
)
async def get_persona_proyectos(
    persona_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: Session = Depends(get_session),
):
    """Obtiene todos los proyectos de ley presentados por la persona en todos sus periodos."""
    return await politics.get_proyectos_by_persona(persona_id, session, skip, limit)


# ========== CANDIDATURAS Y PROCESOS ELECTORALES ==========


@politics_public_router.get(
    "/procesos-electorales",
    status_code=status.HTTP_200_OK,
    response_model=List[ProcesoElectoralResponse],
    summary="Listar procesos electorales",
)
async def get_procesos_electorales(
    activo: Optional[bool] = Query(
        None, description="Filtrar por procesos activos/inactivos"
    ),
    session: Session = Depends(get_session),
):
    """Obtiene los procesos electorales disponibles (ej: Elecciones 2026)"""
    return await politics.get_procesos_electorales(session, activo)


@politics_public_router.get(
    "/procesos-electorales/{proceso_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProcesoElectoralResponse,
    summary="Detalle de un proceso electoral",
)
async def get_proceso_electoral_detail(
    proceso_id: str,
    session: Session = Depends(get_session),
):
    """Obtiene información detallada de un proceso electoral específico"""
    return await politics.get_proceso_electoral_by_id(proceso_id, session)


@politics_public_router.get(
    "/candidaturas",
    status_code=status.HTTP_200_OK,
    response_model=List[CandidaturaDetailResponse],
    summary="Listar candidaturas con filtros",
    description="Endpoint principal para ver candidatos de las Elecciones 2026",
)
async def get_candidaturas_list(
    proceso_electoral_id: Optional[str] = Query(None),
    tipo: Optional[TipoCandidatura] = Query(None),
    partidos: Optional[List[str]] = Query(None),
    distritos: Optional[List[str]] = Query(None),
    estado: Optional[EstadoCandidatura] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session),
):
    """
    Obtiene lista de candidaturas para mostrar en el frontend.
    Útil para mostrar candidatos a Senadores, Diputados, etc.
    """
    return await politics.get_candidaturas_list(
        session=session,
        proceso_electoral_id=proceso_electoral_id,
        tipo=tipo,
        partidos=partidos,
        distritos=distritos,
        estado=estado,
        search=search,
        skip=skip,
        limit=limit,
    )


@politics_public_router.get(
    "/candidaturas/{candidatura_id}",
    status_code=status.HTTP_200_OK,
    response_model=CandidaturaDetailResponse,
    summary="Detalle completo de una candidatura",
)
async def get_candidatura_detail(
    candidatura_id: str, session: Session = Depends(get_session)
):
    """
    Obtiene información detallada de una candidatura específica,
    incluyendo propuestas, plan de gobierno, y datos de la persona.
    """
    return await politics.get_candidatura_by_id(candidatura_id, session)


# ========== PARTIDOS Y DISTRITOS ==========


@politics_public_router.get(
    "/partidos",
    status_code=status.HTTP_200_OK,
    response_model=List[PartidoPoliticoDetailResponse],
    summary="Listar partidos políticos",
)
async def get_partidos(
    activo: bool = Query(True, description="Solo partidos activos"),
    session: Session = Depends(get_session),
):
    """Obtiene la lista de partidos políticos registrados"""
    return await politics.get_partidos_list(session, activo)


@politics_public_router.get(
    "/partidos/{partido_id}",
    status_code=status.HTTP_200_OK,
    response_model=PartidoPoliticoResponse,
    summary="Detalle de un partido político",
)
async def get_partido_detail(partido_id: str, session: Session = Depends(get_session)):
    """Obtiene información detallada de un partido político"""
    return await politics.get_partido_by_id(partido_id, session)


@politics_public_router.get(
    "/distritos",
    status_code=status.HTTP_200_OK,
    response_model=List[DistritoElectoralResponse],
    summary="Listar distritos electorales",
)
async def get_distritos(session: Session = Depends(get_session)):
    """Obtiene la lista de distritos electorales del Perú"""
    return await politics.get_distritos_list(session)


# ====== RUTAS PROTEGIDAS (ADMIN) ======
politics_admin_router = APIRouter(
    prefix="/politics/admin",
    tags=["Politics - Admin"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme), Depends(get_current_user)],
)


def verify_admin(current_user):
    """Helper para verificar permisos de admin"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren permisos de administrador.",
        )


# ========== GESTIÓN DE PERSONAS ==========


@politics_admin_router.post(
    "/personas",
    status_code=status.HTTP_201_CREATED,
    response_model=PersonaDetailResponse,
    summary="Crear nueva persona",
)
async def create_persona(
    data: CreatePersonaRequest,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Crear una nueva persona en el sistema"""
    verify_admin(current_user)
    return await politics.create_persona(data, session)


@politics_admin_router.put(
    "/personas/{persona_id}",
    status_code=status.HTTP_200_OK,
    response_model=PersonaDetailResponse,
    summary="Actualizar datos de persona",
)
async def update_persona(
    persona_id: str,
    data: UpdatePersonaRequest,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Actualizar información biográfica de una persona"""
    verify_admin(current_user)
    return await politics.update_persona(persona_id, data, session)


@politics_admin_router.post(
    "/personas/{persona_id}/periodos-legislativos",
    status_code=status.HTTP_201_CREATED,
    summary="Añadir periodo legislativo a persona",
)
async def add_legislador_periodo(
    persona_id: str,
    data: CreateLegisladorPeriodoRequest,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Asignar un nuevo rol/periodo legislativo a una persona existente"""
    verify_admin(current_user)
    # Aseguramos que el persona_id del path coincida con el del body
    data.persona_id = persona_id
    return await politics.add_legislador_periodo(data, session)


# ========== GESTIÓN DE CANDIDATURAS ==========


@politics_admin_router.post(
    "/candidaturas",
    status_code=status.HTTP_201_CREATED,
    response_model=CandidaturaDetailResponse,
    summary="Crear nueva candidatura",
)
async def create_candidatura(
    data: CreateCandidaturaRequest,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Registrar una nueva candidatura para un proceso electoral"""
    verify_admin(current_user)
    return await politics.add_candidatura(data, session)


@politics_admin_router.put(
    "/candidaturas/{candidatura_id}",
    status_code=status.HTTP_200_OK,
    response_model=CandidaturaDetailResponse,
    summary="Actualizar candidatura",
)
async def update_candidatura(
    candidatura_id: str,
    data: CreateCandidaturaRequest,  # Puedes crear un UpdateCandidaturaRequest específico
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Actualizar información de una candidatura existente"""
    verify_admin(current_user)
    return await politics.update_candidatura(candidatura_id, data, session)


# ========== GESTIÓN DE PARTIDOS ==========


@politics_admin_router.post(
    "/partidos",
    status_code=status.HTTP_201_CREATED,
    response_model=PartidoPoliticoResponse,
    summary="Crear partido político",
)
async def create_partido(
    data: CreatePartidoRequest,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Registrar un nuevo partido político"""
    verify_admin(current_user)
    return await politics.create_partido(data, session)


# ========== GESTIÓN DE PROCESOS ELECTORALES ==========


@politics_admin_router.post(
    "/procesos-electorales",
    status_code=status.HTTP_201_CREATED,
    response_model=ProcesoElectoralResponse,
    summary="Crear proceso electoral",
)
async def create_proceso_electoral(
    data: CreateProcesoElectoralRequest,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Crear un nuevo proceso electoral"""
    verify_admin(current_user)
    return await politics.create_proceso_electoral(data, session)
