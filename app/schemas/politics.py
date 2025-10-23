from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.politics import (
    EstadoCandidatura,
    TipoCamara,
    TipoCandidatura,
)

# ==============================================================================
# == SCHEMAS PARA PERSONA
# ==============================================================================


class CreatePersonaRequest(BaseModel):
    """Request para crear una nueva persona"""

    dni: str = Field(..., max_length=20, description="DNI único de la persona")
    nombres: str = Field(..., max_length=150)
    apellidos: str = Field(..., max_length=150)

    # Datos opcionales
    foto_url: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    profesion: Optional[str] = Field(None, max_length=200)
    biografia_corta: Optional[str] = None
    educacion_superior: Optional[str] = Field(None, max_length=300)

    # Antecedentes
    tiene_antecedentes_penales: bool = False
    tiene_antecedentes_judiciales: bool = False
    resumen_antecedentes: Optional[str] = None

    # Redes sociales
    facebook_url: Optional[str] = None
    twitter_url: Optional[str] = None
    instagram_url: Optional[str] = None


class UpdatePersonaRequest(BaseModel):
    """Request para actualizar una persona"""

    nombres: Optional[str] = Field(None, max_length=150)
    apellidos: Optional[str] = Field(None, max_length=150)
    foto_url: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    profesion: Optional[str] = Field(None, max_length=200)
    biografia_corta: Optional[str] = None
    educacion_superior: Optional[str] = Field(None, max_length=300)

    # Antecedentes
    tiene_antecedentes_penales: Optional[bool] = None
    tiene_antecedentes_judiciales: Optional[bool] = None
    resumen_antecedentes: Optional[str] = None

    # Redes sociales
    facebook_url: Optional[str] = None
    twitter_url: Optional[str] = None
    instagram_url: Optional[str] = None


# ==============================================================================
# == LEGISLADOR (PERIODO)
# ==============================================================================


class CreateLegisladorPeriodoRequest(BaseModel):
    """Request para añadir un periodo legislativo a una persona"""

    persona_id: str = Field(..., description="ID de la persona")
    partido_id: str = Field(..., description="ID del partido político")
    distrito_id: str = Field(..., description="ID del distrito electoral")
    camara: TipoCamara = Field(..., description="Tipo de cámara legislativa")
    periodo_inicio: datetime = Field(..., description="Fecha de inicio del periodo")
    periodo_fin: datetime = Field(..., description="Fecha de fin del periodo")
    esta_activo: bool = Field(True, description="Si el periodo está activo")
    email_congreso: Optional[str] = Field(None, max_length=255)


# ==============================================================================
# == CANDIDATURA
# ==============================================================================


class CreateCandidaturaRequest(BaseModel):
    """Request para crear una nueva candidatura"""

    persona_id: str = Field(..., description="ID de la persona que se postula")
    proceso_electoral_id: str = Field(..., description="ID del proceso electoral")
    tipo: TipoCandidatura = Field(..., description="Tipo de candidatura")
    partido_id: str = Field(..., description="ID del partido político")
    distrito_id: Optional[str] = Field(
        None, description="ID del distrito (no aplica para Presidente/Vicepresidente)"
    )
    numero_lista: Optional[int] = Field(
        None, description="Posición en la lista del partido"
    )

    # Propuestas y documentos
    propuestas: Optional[str] = Field(None, description="Propuestas del candidato")
    plan_gobierno_url: Optional[str] = Field(
        None, description="URL del plan de gobierno"
    )
    hoja_vida_url: Optional[str] = Field(None, description="URL de la hoja de vida")

    # Estado
    estado: EstadoCandidatura = Field(
        EstadoCandidatura.INSCRITO, description="Estado de la candidatura"
    )

    # Resultados
    votos_obtenidos: Optional[int] = None
    fue_elegido: bool = False


class UpdateCandidaturaRequest(BaseModel):
    """Request para actualizar una candidatura"""

    tipo: Optional[TipoCandidatura] = None
    partido_id: Optional[str] = None
    distrito_id: Optional[str] = None
    numero_lista: Optional[int] = None
    propuestas: Optional[str] = None
    plan_gobierno_url: Optional[str] = None
    hoja_vida_url: Optional[str] = None
    estado: Optional[EstadoCandidatura] = None
    votos_obtenidos: Optional[int] = None
    fue_elegido: Optional[bool] = None


# ==============================================================================
# == PARTIDO POLÍTICO
# ==============================================================================


class CreatePartidoRequest(BaseModel):
    """Request para crear un nuevo partido político"""

    nombre: str = Field(..., max_length=200, description="Nombre completo del partido")
    sigla: str = Field(..., max_length=20, description="Sigla o acrónimo")
    logo_url: Optional[str] = Field(None, description="URL del logo del partido")
    color_hex: Optional[str] = Field(
        None,
        max_length=7,
        description="Color representativo en formato hexadecimal (#RRGGBB)",
    )
    activo: bool = Field(True, description="Si el partido está activo")


class UpdatePartidoRequest(BaseModel):
    """Request para actualizar un partido político"""

    nombre: Optional[str] = Field(None, max_length=200)
    sigla: Optional[str] = Field(None, max_length=20)
    logo_url: Optional[str] = None
    color_hex: Optional[str] = Field(None, max_length=7)
    activo: Optional[bool] = None


# ==============================================================================
# == DISTRITO
# ==============================================================================


class CreateDistritoRequest(BaseModel):
    """Request para crear un nuevo distrito electoral"""

    nombre: str = Field(..., max_length=100, description="Nombre del distrito")
    codigo: str = Field(..., max_length=10, description="Código del distrito")
    es_distrito_nacional: bool = Field(False, description="Si es un distrito nacional")
    num_senadores: int = Field(0, description="Número de senadores a elegir")
    num_diputados: int = Field(0, description="Número de diputados a elegir")
    activo: bool = Field(True, description="Si el distrito está activo")


# ==============================================================================
# == PROCESO ELECTORAL
# ==============================================================================


class CreateProcesoElectoralRequest(BaseModel):
    """Request para crear un nuevo proceso electoral"""

    nombre: str = Field(..., max_length=200, description="Nombre del proceso electoral")
    año: int = Field(..., description="Año del proceso electoral")
    fecha_elecciones: datetime = Field(..., description="Fecha de las elecciones")
    activo: bool = Field(True, description="Si el proceso está activo")


class UpdateProcesoElectoralRequest(BaseModel):
    """Request para actualizar un proceso electoral"""

    nombre: Optional[str] = Field(None, max_length=200)
    fecha_elecciones: Optional[datetime] = None
    activo: Optional[bool] = None


# ==============================================================================
# == PROYECTO DE LEY
# ==============================================================================


class CreateProyectoLeyRequest(BaseModel):
    """Request para crear un nuevo proyecto de ley"""

    legislador_id: str = Field(..., description="ID del legislador autor")
    numero: str = Field(..., max_length=50, description="Número del proyecto")
    titulo: str = Field(..., max_length=500, description="Título del proyecto")
    resumen: str = Field(..., description="Resumen del proyecto")
    fecha_presentacion: datetime = Field(..., description="Fecha de presentación")
    estado: str = Field(..., max_length=100, description="Estado actual")
    url_documento: Optional[str] = Field(None, description="URL del documento")


# ==============================================================================
# == DENUNCIA
# ==============================================================================


class CreateDenunciaRequest(BaseModel):
    """Request para crear una nueva denuncia"""

    legislador_id: str = Field(..., description="ID del legislador denunciado")
    titulo: str = Field(..., max_length=300, description="Título de la denuncia")
    descripcion: str = Field(..., description="Descripción detallada")
    tipo: str = Field(..., max_length=100, description="Tipo de denuncia")
    fecha_denuncia: datetime = Field(..., description="Fecha de la denuncia")
    estado: str = Field(..., description="Estado actual de la denuncia")
    resolucion: Optional[str] = Field(None, description="Resolución de la denuncia")
    url_documento: Optional[str] = Field(None, description="URL del documento")
