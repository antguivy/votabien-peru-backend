from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel

from app.models.politics import (
    Antecedente,
    EstadoCandidatura,
    HistorialPartido,
    TipoCamara,
    TipoCandidatura,
)

# ==============================================================================
# == PERSONA
# ==============================================================================


class PersonaBaseResponse(BaseModel):
    """Información básica de una persona"""

    id: str
    dni: str
    nombres: str
    apellidos: str
    nombre_completo: str
    foto_url: Optional[str] = None
    profesion: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    biografia_corta: Optional[str] = None

    # Educacion
    educacion_tecnica: Optional[str] = None
    educacion_universitaria: Optional[str] = None
    grado_academico: Optional[str] = None
    titulo_profesional: Optional[str] = None
    post_grado: Optional[str] = None
    hoja_vida_url: Optional[str] = None

    # Antecedentes
    antecedentes_penales: Optional[List[Antecedente]] = []
    antecedentes_judiciales: Optional[List[Antecedente]] = []

    # Redes sociales
    facebook_url: Optional[str] = None
    twitter_url: Optional[str] = None
    instagram_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PeriodoLegisladorResponse(BaseModel):
    """Información de un periodo legislativo"""

    id: str
    camara: TipoCamara
    periodo_inicio: datetime
    periodo_fin: datetime
    esta_activo: bool
    partido: "PartidoPoliticoResponse"
    distrito: "DistritoElectoralResponse"
    proyectos_ley: List["ProyectoLeyResponse"] = []

    class Config:
        from_attributes = True


class PersonaListResponse(PersonaBaseResponse):
    """
    Response para lista de personas.
    Incluye el periodo legislativo activo si existe.
    """

    periodo_activo: Optional[PeriodoLegisladorResponse] = None
    antecedentes_penales: Optional[List[Antecedente]] = []
    antecedentes_judiciales: Optional[List[Antecedente]] = []


class PersonaDetailResponse(PersonaBaseResponse):
    """
    Response completo de una persona con todo su historial.
    """

    # Historial político
    periodos_legislativos: List[PeriodoLegisladorResponse] = []
    candidaturas: List["CandidaturaListResponse"] = []

    created_at: datetime


# ==============================================================================
# == CANDIDATURAS
# ==============================================================================


class CandidaturaBaseResponse(BaseModel):
    """Información básica de una candidatura"""

    id: str
    tipo: TipoCandidatura
    numero_lista: Optional[int] = None
    estado: EstadoCandidatura
    votos_obtenidos: Optional[int] = None
    fue_elegido: bool = False

    class Config:
        from_attributes = True


class CandidaturaListResponse(CandidaturaBaseResponse):
    """
    Response para lista de candidaturas.
    Incluye información resumida de persona, partido, distrito.
    """

    persona: "PersonaBaseResponse"
    partido: "PartidoPoliticoResponse"
    distrito: Optional["DistritoElectoralResponse"] = None
    proceso_electoral: "ProcesoElectoralResponse"


class CandidaturaDetailResponse(CandidaturaBaseResponse):
    """
    Response completo de una candidatura con propuestas y planes.
    """

    persona: "PersonaBaseResponse"
    periodos_legislativos: List[PeriodoLegisladorResponse] = []
    partido: "PartidoPoliticoResponse"
    distrito: Optional["DistritoElectoralResponse"] = None
    proceso_electoral: "ProcesoElectoralResponse"

    # Propuestas y documentos
    propuestas: Optional[str] = None
    plan_gobierno_url: Optional[str] = None

    created_at: datetime


# ==============================================================================
# == PARTIDOS
# ==============================================================================


class PartidoPoliticoResponse(BaseModel):
    """Información de un partido político"""

    id: str
    nombre: str
    sigla: str
    logo_url: Optional[str] = None
    color_hex: Optional[str] = None
    activo: bool = True
    created_at: datetime

    class Config:
        from_attributes = True


class PartidoPoliticoDetailResponse(BaseModel):
    """Información detallada de un partido político"""

    id: str
    nombre: str
    sigla: str
    logo_url: Optional[str] = None
    color_hex: Optional[str] = None
    activo: bool

    fundador: Optional[str] = None
    fecha_fundacion: Optional[date] = None
    descripcion: Optional[str] = None
    ideologia: Optional[str] = None
    sede_nacional: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    sitio_web: Optional[str] = None

    financiamiento_anual: Optional[float] = None
    gasto_campana_ultima: Optional[float] = None
    fuente_financiamiento: Optional[str] = None
    historia_timeline: Optional[list[HistorialPartido]] = []  # ya parseado desde JSON

    facebook_url: Optional[str] = None
    twitter_url: Optional[str] = None
    instagram_url: Optional[str] = None
    youtube_url: Optional[str] = None

    total_militantes: Optional[int] = None
    total_escaños: Optional[int] = None

    created_at: datetime

    class Config:
        from_attributes = True


# ==============================================================================
# == DISTRITOS
# ==============================================================================


class DistritoElectoralResponse(BaseModel):
    """Información de un distrito electoral"""

    id: str
    nombre: str
    codigo: str
    es_distrito_nacional: bool = False
    num_senadores: int = 0
    num_diputados: int = 0
    activo: bool = True

    class Config:
        from_attributes = True


# ==============================================================================
# == PROCESOS ELECTORALES
# ==============================================================================


class ProcesoElectoralResponse(BaseModel):
    """Información de un proceso electoral"""

    id: str
    nombre: str
    año: int
    fecha_elecciones: datetime
    activo: bool = True
    created_at: datetime

    class Config:
        from_attributes = True


# ==============================================================================
# == PROYECTOS DE LEY
# ==============================================================================


class ProyectoLeyResponse(BaseModel):
    """Información de un proyecto de ley"""

    id: str
    numero: str
    titulo: str
    resumen: str
    fecha_presentacion: datetime
    estado: str
    url_documento: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ==============================================================================
# == ASISTENCIAS
# ==============================================================================


class AsistenciaResponse(BaseModel):
    """Registro de asistencia a sesión"""

    id: str
    fecha: datetime
    tipo_sesion: str
    asistio: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==============================================================================
# == DENUNCIAS
# ==============================================================================


class DenunciaResponse(BaseModel):
    """Información de una denuncia"""

    id: str
    titulo: str
    descripcion: str
    tipo: str
    fecha_denuncia: datetime
    estado: str
    resolucion: Optional[str] = None
    url_documento: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ==============================================================================
# == ESTADÍSTICAS
# ==============================================================================


class EstadisticasLegisladorResponse(BaseModel):
    """Estadísticas de desempeño de un legislador"""

    total_proyectos_ley: int = 0
    proyectos_aprobados: int = 0
    tasa_asistencia: float = 0.0
    total_denuncias: int = 0
    denuncias_activas: int = 0


# Resolver referencias circulares
PersonaDetailResponse.model_rebuild()
CandidaturaListResponse.model_rebuild()
CandidaturaDetailResponse.model_rebuild()
PeriodoLegisladorResponse.model_rebuild()
