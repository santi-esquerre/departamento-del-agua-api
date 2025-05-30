from datetime import date, datetime
from typing import List, Optional
from pydantic import ConfigDict, BaseModel, Field, EmailStr


# Esquemas base para Personal
class PersonalBase(BaseModel):
    nombre: str
    cargo: Optional[str] = None
    descripcion: Optional[str] = None
    foto_url: Optional[str] = None
    cv_url: Optional[str] = None
    orcid: Optional[str] = None
    email: Optional[EmailStr] = None
    fecha_alta: Optional[date] = None


class PersonalCreate(PersonalBase):
    pass


class PersonalRead(PersonalBase):
    id: int
    fecha_baja: Optional[date] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PersonalUpdate(BaseModel):
    nombre: Optional[str] = None
    cargo: Optional[str] = None
    descripcion: Optional[str] = None
    foto_url: Optional[str] = None
    cv_url: Optional[str] = None
    orcid: Optional[str] = None
    email: Optional[str] = None
    fecha_alta: Optional[date] = None
    fecha_baja: Optional[date] = None


# Esquemas para relaciones
class PersonalProyectoBase(BaseModel):
    personal_id: int
    proyecto_id: int
    rol: Optional[str] = None


class PersonalProyectoCreate(PersonalProyectoBase):
    pass


class PersonalProyectoRead(PersonalProyectoBase):
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
