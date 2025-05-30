# app/models/models.py

from datetime import date, datetime, timezone
from typing import List, Optional
from sqlmodel import Field, JSON, Relationship, SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Personal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    cargo: Optional[str]
    descripcion: Optional[str]
    foto_url: Optional[str]
    cv_url: Optional[str]
    orcid: Optional[str]
    email: Optional[str]
    fecha_alta: Optional[date]
    fecha_baja: Optional[date]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    proyectos: List["PersonalProyecto"] = Relationship(back_populates="personal")


class Publicacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    cita_formateada: Optional[str] = None
    doi_url: Optional[str] = None
    enlace_pdf: Optional[str] = None
    anio: Optional[int] = None
    estado: Optional[str] = None
    fecha_registro: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    authors: List[dict] = Field(
        sa_column=Column(JSON), default_factory=list
    )  # Use JSON for cross-db compatibility
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Proyecto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str]
    fecha_inicio: Optional[date]
    fecha_fin: Optional[date]
    financiador: Optional[str]
    presupuesto: Optional[float]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    personal: List["PersonalProyecto"] = Relationship(back_populates="proyecto")


class PersonalProyecto(SQLModel, table=True):
    personal_id: int = Field(foreign_key="personal.id", primary_key=True)
    proyecto_id: int = Field(foreign_key="proyecto.id", primary_key=True)
    rol: Optional[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    personal: "Personal" = Relationship(back_populates="proyectos")
    proyecto: "Proyecto" = Relationship(back_populates="personal")


class Actividad(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: Optional[str]
    descripcion: Optional[str]
    fecha: Optional[date]
    resultado_url: Optional[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    equipamientos: List["EquipamientoActividad"] = Relationship(
        back_populates="actividad"
    )


class Equipamiento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    marca: Optional[str]
    modelo: Optional[str]
    n_serie: Optional[str]
    hoja_especificaciones_url: Optional[str]
    fecha_adquisicion: Optional[date]
    estado: Optional[str]
    ubicacion: Optional[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    actividades: List["EquipamientoActividad"] = Relationship(
        back_populates="equipamiento"
    )
    servicios: List["ServicioEquipamiento"] = Relationship(
        back_populates="equipamiento"
    )


class EquipamientoActividad(SQLModel, table=True):
    equipamiento_id: int = Field(foreign_key="equipamiento.id", primary_key=True)
    actividad_id: int = Field(foreign_key="actividad.id", primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    equipamiento: "Equipamiento" = Relationship(back_populates="actividades")
    actividad: "Actividad" = Relationship(back_populates="equipamientos")


class Servicio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str]
    publico_objetivo: Optional[str]
    tarifa: Optional[float]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    equipamientos: List["ServicioEquipamiento"] = Relationship(
        back_populates="servicio"
    )


class ServicioEquipamiento(SQLModel, table=True):
    servicio_id: int = Field(foreign_key="servicio.id", primary_key=True)
    equipamiento_id: int = Field(foreign_key="equipamiento.id", primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    servicio: "Servicio" = Relationship(back_populates="equipamientos")
    equipamiento: "Equipamiento" = Relationship(back_populates="servicios")


class Archivo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    ruta: str
    tipo: Optional[str]
    tamano: Optional[int]
    fecha_subida: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
