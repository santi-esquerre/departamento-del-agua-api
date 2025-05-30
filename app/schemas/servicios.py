from datetime import datetime
from typing import List, Optional
from pydantic import ConfigDict, BaseModel, Field


# Esquemas base para Servicio
class ServicioBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    publico_objetivo: Optional[str] = None
    tarifa: Optional[float] = Field(default=None, ge=0)  # Add ge=0 validation


class ServicioCreate(ServicioBase):
    equipamiento_ids: List[int | None]  # Requiere al menos un equipamiento asignado


class ServicioRead(ServicioBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ServicioUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    publico_objetivo: Optional[str] = None
    tarifa: Optional[float] = None
    equipamiento_ids: Optional[List[int]] = (
        None  # Para reemplazar el conjunto de equipamiento
    )


# Esquemas para relaciones
class ServicioEquipamientoBase(BaseModel):
    servicio_id: int
    equipamiento_id: int


class ServicioEquipamientoCreate(ServicioEquipamientoBase):
    pass


class ServicioEquipamientoRead(ServicioEquipamientoBase):
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
