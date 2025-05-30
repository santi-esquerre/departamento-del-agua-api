# app/schemas/academico.py

from datetime import datetime
from typing import List, Optional
from pydantic import ConfigDict, BaseModel, Field, validator
from enum import Enum


class TipoRequisitoEnum(str, Enum):
    PREREQUISITO = "prerequisito"
    CORREQUISITO = "correquisito"


# Carrera Schemas
class CarreraBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    titulo_otorgado: Optional[str] = None
    duracion_anios: Optional[int] = None


class CarreraCreate(CarreraBase):
    pass


class CarreraRead(CarreraBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CarreraUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    titulo_otorgado: Optional[str] = None
    duracion_anios: Optional[int] = None


# Materia Schemas
class MateriaBase(BaseModel):
    nombre: str
    codigo: str
    descripcion: Optional[str] = None
    semestre: int
    creditos: Optional[int] = None
    programa_pdf_url: Optional[str] = None
    id_carrera: int


class MateriaCreate(MateriaBase):
    pass


class MateriaRead(MateriaBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class MateriaUpdate(BaseModel):
    nombre: Optional[str] = None
    codigo: Optional[str] = None
    descripcion: Optional[str] = None
    semestre: Optional[int] = None
    creditos: Optional[int] = None
    programa_pdf_url: Optional[str] = None
    id_carrera: Optional[int] = None


# Requisito Schemas
class RequisitoBase(BaseModel):
    id_materia: int
    id_materia_requisito: int
    tipo: TipoRequisitoEnum = TipoRequisitoEnum.PREREQUISITO


class RequisitoCreate(RequisitoBase):
    pass


class RequisitoRead(RequisitoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class RequisitoUpdate(BaseModel):
    id_materia: Optional[int] = None
    id_materia_requisito: Optional[int] = None
    tipo: Optional[TipoRequisitoEnum] = None


# Schemas with relationships
class MateriaWithRelacionesRead(MateriaRead):
    carrera: Optional[CarreraRead] = None
    requisitos_de: List[RequisitoRead] = []
    requisito_para: List[RequisitoRead] = []
    model_config = ConfigDict(from_attributes=True)


class CarreraWithMateriasRead(CarreraRead):
    materias: List[MateriaRead] = []
    model_config = ConfigDict(from_attributes=True)
