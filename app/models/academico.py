# app/models/academico.py

from datetime import datetime, timezone
from typing import List, Optional
from enum import Enum, auto
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, DateTime


class TipoRequisito(str, Enum):
    PREREQUISITO = "prerequisito"
    CORREQUISITO = "correquisito"


class Carrera(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None
    titulo_otorgado: Optional[str] = None
    duracion_anios: Optional[int] = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )

    # Relaciones
    materias: List["Materia"] = Relationship(back_populates="carrera")


class Materia(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    codigo: str
    descripcion: Optional[str] = None
    semestre: int
    creditos: Optional[int] = None
    programa_pdf_url: Optional[str] = None
    id_carrera: int = Field(foreign_key="carrera.id")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )

    # Relaciones
    carrera: Carrera = Relationship(back_populates="materias")
    requisitos_de: List["Requisito"] = Relationship(
        back_populates="materia",
        sa_relationship_kwargs={"foreign_keys": "[Requisito.id_materia]"},
    )
    requisito_para: List["Requisito"] = Relationship(
        back_populates="materia_requisito",
        sa_relationship_kwargs={"foreign_keys": "[Requisito.id_materia_requisito]"},
    )


class Requisito(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_materia: int = Field(foreign_key="materia.id")
    id_materia_requisito: int = Field(foreign_key="materia.id")
    tipo: TipoRequisito = Field(default=TipoRequisito.PREREQUISITO)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )

    # Relaciones
    materia: Materia = Relationship(
        back_populates="requisitos_de",
        sa_relationship_kwargs={"foreign_keys": "[Requisito.id_materia]"},
    )
    materia_requisito: Materia = Relationship(
        back_populates="requisito_para",
        sa_relationship_kwargs={"foreign_keys": "[Requisito.id_materia_requisito]"},
    )
