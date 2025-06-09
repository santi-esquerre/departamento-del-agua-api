from datetime import date, datetime
from typing import List, Optional
from pydantic import ConfigDict, BaseModel, Field


# Esquemas base para Equipamiento
class EquipamientoBase(BaseModel):
    nombre: str
    marca: Optional[str] = None
    modelo: Optional[str] = None
    n_serie: Optional[str] = None
    hoja_especificaciones_url: Optional[str] = None
    fecha_adquisicion: Optional[date] = None
    estado: Optional[str] = None
    ubicacion: Optional[str] = None


class EquipamientoCreate(EquipamientoBase):
    pass


class EquipamientoRead(EquipamientoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class EquipamientoUpdate(BaseModel):
    nombre: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    n_serie: Optional[str] = None
    hoja_especificaciones_url: Optional[str] = None
    fecha_adquisicion: Optional[date] = None
    estado: Optional[str] = None
    ubicacion: Optional[str] = None


# Esquemas para relaciones con Actividades
class EquipamientoActividadBase(BaseModel):
    equipamiento_id: int
    actividad_id: int


class EquipamientoActividadCreate(EquipamientoActividadBase):
    pass


class EquipamientoActividadRead(EquipamientoActividadBase):
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
