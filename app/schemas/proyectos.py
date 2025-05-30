from datetime import date, datetime
from typing import List, Optional
from pydantic import ConfigDict, BaseModel, Field, validator


# Esquemas base para Proyecto
class ProyectoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    financiador: Optional[str] = None
    presupuesto: Optional[float] = None

    # TODO[pydantic]: We couldn't refactor the `validator`, please replace it by `field_validator` manually.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-validators for more information.
    @validator("fecha_fin")
    def validate_fecha_fin(cls, v, values):
        if v and values.get("fecha_inicio") and v < values["fecha_inicio"]:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")
        return v


class ProyectoCreate(ProyectoBase):
    pass


class ProyectoRead(ProyectoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    financiador: Optional[str] = None
    presupuesto: Optional[float] = None

    # TODO[pydantic]: We couldn't refactor the `validator`, please replace it by `field_validator` manually.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-validators for more information.
    @validator("fecha_fin")
    def validate_fecha_fin(cls, v, values):
        if v and values.get("fecha_inicio") and v < values["fecha_inicio"]:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")
        return v


# Esquemas para la relación Personal-Proyecto
class ProyectoPersonalCreate(BaseModel):
    personal_id: int
    rol: Optional[str] = None


class ProyectoPersonalRead(BaseModel):
    personal_id: int
    proyecto_id: int
    rol: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
