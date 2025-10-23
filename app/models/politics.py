from datetime import date, datetime, timezone
from enum import Enum
from typing import List, Optional

from cuid2 import Cuid
from pydantic import BaseModel
from sqlmodel import JSON, Column, DateTime, Field, Relationship, SQLModel, Text


def cuid_factory():
    return Cuid().generate()


def utc_now():
    return datetime.now(timezone.utc)


# ============= ENUMS =============
class TipoCamara(str, Enum):
    CONGRESO = "Congreso"
    SENADO = "Senado"
    DIPUTADOS = "Diputados"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member


class TipoCandidatura(str, Enum):
    PRESIDENTE = "Presidente"
    VICEPRESIDENTE = "Vicepresidente"
    SENADOR = "Senador"
    DIPUTADO = "Diputado"
    CONGRESISTA = "Congresista"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member


class EstadoCandidatura(str, Enum):
    INSCRITO = "Inscrito"
    HABIL = "Hábil"
    INHABILITADO = "Inhabilitado"
    TACADO = "Tacado"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member


# ============= MODELOS CENTRALES =============
class Antecedente(BaseModel):
    tipo: str
    descripcion: str
    estado: Optional[str] = None
    año: Optional[int] = None


class ExperienciaLaboral(BaseModel):
    cargo: Optional[str] = None
    empresa: Optional[str] = None
    periodo: Optional[str] = None
    descripcion: Optional[str] = None


# --- Entidad central Persona ---
class Persona(SQLModel, table=True):
    """
    Entidad única que representa a un individuo en la política.
    Almacena información biográfica que no cambia entre candidaturas o periodos.
    """

    id: str = Field(default_factory=cuid_factory, primary_key=True)

    # Identificación básica y única
    dni: str = Field(unique=True, max_length=20, index=True)
    nombres: str = Field(max_length=150)
    apellidos: str = Field(max_length=150)
    nombre_completo: str = Field(max_length=300, index=True)  # Para búsquedas

    # Datos biográficos
    foto_url: Optional[str] = Field(default=None)
    fecha_nacimiento: Optional[datetime] = Field(default=None)
    profesion: Optional[str] = Field(default=None, max_length=200)
    biografia_corta: Optional[str] = Field(default=None, sa_column=Column(Text))

    # Educacion
    educacion_tecnica: Optional[str] = Field(default=None, max_length=300)
    educacion_universitaria: Optional[str] = Field(default=None, max_length=300)
    grado_academico: Optional[str] = Field(default=None, max_length=300)
    titulo_profesional: Optional[str] = Field(default=None, max_length=300)
    post_grado: Optional[str] = Field(default=None, max_length=300)
    hoja_vida_url: Optional[str] = Field(default=None)
    experiencia_laboral: Optional[List[ExperienciaLaboral]] = Field(
        default=None, sa_column=Column(JSON)
    )
    # Antecedentes
    antecedentes_penales: Optional[List[Antecedente]] = Field(
        default=None, sa_column=Column(JSON)
    )
    antecedentes_judiciales: Optional[List[Antecedente]] = Field(
        default=None, sa_column=Column(JSON)
    )

    # Redes sociales
    facebook_url: Optional[str] = Field(default=None)
    twitter_url: Optional[str] = Field(default=None)
    instagram_url: Optional[str] = Field(default=None)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=utc_now,
    )

    # Relaciones: Una persona puede tener múltiples roles a lo largo del tiempo
    periodos_legislativos: List["Legislador"] = Relationship(back_populates="persona")
    candidaturas: List["Candidato"] = Relationship(back_populates="persona")


class HistorialPartido(BaseModel):
    año: int
    evento: str


class PartidoPolitico(SQLModel, table=True):
    """Organizaciones políticas que presentan candidatos"""

    id: str = Field(default_factory=cuid_factory, primary_key=True)
    nombre: str = Field(max_length=200, unique=True, index=True)
    sigla: str = Field(max_length=20, index=True)
    logo_url: Optional[str] = Field(default=None)
    color_hex: Optional[str] = Field(default=None, max_length=7)
    activo: bool = Field(default=True)

    fundador: Optional[str] = Field(default=None, max_length=200)
    fecha_fundacion: Optional[date] = Field(default=None)
    descripcion: Optional[str] = Field(default=None, max_length=1000)
    ideologia: Optional[str] = Field(
        default=None, max_length=200
    )  # ej: "Centro-izquierda", "Derecha liberal"
    sede_nacional: Optional[str] = Field(default=None, max_length=300)
    telefono: Optional[str] = Field(default=None, max_length=50)
    email: Optional[str] = Field(default=None, max_length=100)
    sitio_web: Optional[str] = Field(default=None, max_length=200)

    # Campos de financiamiento y gastos (en soles)
    financiamiento_anual: Optional[float] = Field(default=None)
    gasto_campana_ultima: Optional[float] = Field(default=None)
    fuente_financiamiento: Optional[str] = Field(default=None, max_length=500)

    # Timeline e historia (almacenado como JSON)
    historia_timeline: Optional[List[HistorialPartido]] = Field(
        default=None, sa_column=Column(JSON)
    )  # JSON string

    # Redes sociales
    facebook_url: Optional[str] = Field(default=None)
    twitter_url: Optional[str] = Field(default=None)
    instagram_url: Optional[str] = Field(default=None)
    youtube_url: Optional[str] = Field(default=None)

    # Estadísticas
    total_militantes: Optional[int] = Field(default=None)
    total_escaños: Optional[int] = Field(default=None)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=utc_now,
    )

    # Relaciones
    legisladores: List["Legislador"] = Relationship(back_populates="partido")
    candidatos: List["Candidato"] = Relationship(back_populates="partido")


class Distrito(SQLModel, table=True):
    """Distritos electorales de Perú."""

    id: str = Field(default_factory=cuid_factory, primary_key=True)
    nombre: str = Field(max_length=100, unique=True, index=True)
    codigo: str = Field(max_length=10, unique=True)
    es_distrito_nacional: bool = Field(default=False)
    num_senadores: int = Field(default=0)
    num_diputados: int = Field(default=0)
    activo: bool = Field(default=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=utc_now,
    )

    # Relaciones
    legisladores: List["Legislador"] = Relationship(back_populates="distrito")
    candidatos: List["Candidato"] = Relationship(back_populates="distrito")


class ProcesoElectoral(SQLModel, table=True):
    """Define un evento electoral específico."""

    id: str = Field(default_factory=cuid_factory, primary_key=True)
    nombre: str = Field(max_length=200)  # "Elecciones Generales 2026"
    año: int = Field(index=True)
    fecha_elecciones: datetime
    activo: bool = Field(default=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=utc_now,
    )

    # Relaciones
    candidaturas: List["Candidato"] = Relationship(back_populates="proceso_electoral")


# ============= MODELOS DE ROLES =============


class Legislador(SQLModel, table=True):
    """
    Representa UN PERIODO en el que una Persona sirvió como legislador.
    Una persona puede tener varios de estos registros si fue reelegida.
    """

    id: str = Field(default_factory=cuid_factory, primary_key=True)
    persona_id: str = Field(foreign_key="persona.id", index=True)

    # Información del cargo en este periodo específico
    partido_id: str = Field(foreign_key="partidopolitico.id", index=True)
    distrito_id: str = Field(foreign_key="distrito.id", index=True)
    camara: TipoCamara
    periodo_inicio: datetime
    periodo_fin: datetime
    esta_activo: bool = Field(default=True)  # Si está actualmente en el cargo
    email_congreso: Optional[str] = Field(default=None, max_length=255)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=utc_now,
    )

    # Relaciones
    persona: "Persona" = Relationship(back_populates="periodos_legislativos")
    partido: "PartidoPolitico" = Relationship(back_populates="legisladores")
    distrito: "Distrito" = Relationship(back_populates="legisladores")

    # El desempeño legislativo está atado a un periodo específico
    proyectos_ley: List["ProyectoLey"] = Relationship(back_populates="autor")
    asistencias: List["Asistencia"] = Relationship(back_populates="legislador")
    denuncias: List["Denuncia"] = Relationship(back_populates="legislador")


class Candidato(SQLModel, table=True):
    """
    Representa UNA POSTULACIÓN de una Persona a un cargo en un ProcesoElectoral.
    """

    id: str = Field(default_factory=cuid_factory, primary_key=True)
    persona_id: str = Field(foreign_key="persona.id", index=True)
    proceso_electoral_id: str = Field(foreign_key="procesoelectoral.id", index=True)

    # Información específica de esta candidatura
    tipo: TipoCandidatura = Field(index=True)
    partido_id: str = Field(foreign_key="partidopolitico.id", index=True)
    distrito_id: Optional[str] = Field(
        default=None, foreign_key="distrito.id"
    )  # Null para Presidente/Vice
    numero_lista: Optional[int] = Field(default=None)

    # Propuestas y planes para esta elección
    propuestas: Optional[str] = Field(default=None, sa_column=Column(Text))
    plan_gobierno_url: Optional[str] = Field(default=None)

    # Estado de la candidatura en este proceso
    estado: EstadoCandidatura = Field(default=EstadoCandidatura.INSCRITO)

    # Resultados
    votos_obtenidos: Optional[int] = Field(default=None)
    fue_elegido: bool = Field(default=False)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=utc_now,
    )

    # Relaciones
    persona: "Persona" = Relationship(back_populates="candidaturas")
    partido: "PartidoPolitico" = Relationship(back_populates="candidatos")
    distrito: Optional["Distrito"] = Relationship(back_populates="candidatos")
    proceso_electoral: "ProcesoElectoral" = Relationship(back_populates="candidaturas")


# ============= DESEMPEÑO LEGISLATIVO =============


class ProyectoLey(SQLModel, table=True):
    """Proyectos de ley presentados por un legislador en un periodo concreto"""

    id: str = Field(default_factory=cuid_factory, primary_key=True)
    legislador_id: str = Field(foreign_key="legislador.id", index=True)
    numero: str = Field(max_length=50, unique=True, index=True)
    titulo: str = Field(max_length=500)
    resumen: str = Field(sa_column=Column(Text))
    fecha_presentacion: datetime
    estado: str = Field(max_length=100)
    url_documento: Optional[str] = Field(default=None)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=utc_now,
    )

    autor: "Legislador" = Relationship(back_populates="proyectos_ley")


class Asistencia(SQLModel, table=True):
    """Registro de asistencias a sesiones durante un periodo legislativo"""

    id: str = Field(default_factory=cuid_factory, primary_key=True)
    legislador_id: str = Field(foreign_key="legislador.id", index=True)
    fecha: datetime = Field(index=True)
    tipo_sesion: str
    asistio: bool
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=utc_now,
    )

    legislador: "Legislador" = Relationship(back_populates="asistencias")


class Denuncia(SQLModel, table=True):
    """Denuncias contra un legislador durante su periodo"""

    id: str = Field(default_factory=cuid_factory, primary_key=True)
    legislador_id: str = Field(foreign_key="legislador.id", index=True)
    titulo: str = Field(max_length=300)
    descripcion: str = Field(sa_column=Column(Text))
    tipo: str = Field(max_length=100)
    fecha_denuncia: datetime
    estado: str
    resolucion: Optional[str] = Field(default=None, sa_column=Column(Text))
    url_documento: Optional[str] = Field(default=None)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=utc_now,
    )

    legislador: "Legislador" = Relationship(back_populates="denuncias")
