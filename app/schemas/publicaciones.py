from datetime import datetime
from typing import List, Optional, Dict, Union
from pydantic import field_validator, ConfigDict, BaseModel, Field
import json


# Esquema para autores en JSON
class Author(BaseModel):
    name: str
    personal_id: Optional[int] = None


# Esquemas base para Publicación
class PublicacionBase(BaseModel):
    titulo: str
    cita_formateada: Optional[str] = None
    doi_url: Optional[str] = None
    enlace_pdf: Optional[str] = None
    anio: Optional[int] = None
    estado: Optional[str] = None
    authors: List[Author] = Field(default_factory=list)

    @field_validator("anio")
    @classmethod
    def validate_anio(cls, v):
        if v is not None and (v < 1900 or v > datetime.now().year + 5):
            raise ValueError(f"Año debe estar entre 1900 y {datetime.now().year + 5}")
        return v


class PublicacionCreate(PublicacionBase):
    # Convertir la lista de autores a string JSON para almacenar
    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        return data


class PublicacionRead(PublicacionBase):
    id: int
    fecha_registro: datetime
    created_at: datetime
    updated_at: datetime

    # Convertir el string JSON a lista de autores al leer
    @field_validator("authors", mode="before")
    @classmethod
    def parse_authors(cls, v):
        if isinstance(v, str):
            return json.loads(
                v
            )  # Keep json.loads for compatibility if needed during transition
        return v
    model_config = ConfigDict(from_attributes=True)


class PublicacionUpdate(BaseModel):
    titulo: Optional[str] = None
    cita_formateada: Optional[str] = None
    doi_url: Optional[str] = None
    enlace_pdf: Optional[str] = None
    anio: Optional[int] = None
    estado: Optional[str] = None
    authors: Optional[List[Author]] = None

    # Validar año si se proporciona
    @field_validator("anio")
    @classmethod
    def validate_anio(cls, v):
        if v is not None and (v < 1900 or v > datetime.now().year + 5):
            raise ValueError(f"Año debe estar entre 1900 y {datetime.now().year + 5}")
        return v

    # Convertir la lista de autores a string JSON para almacenar
    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        if data.get("authors") is not None:
            pass  # Authors will be handled as a list of dicts
        return data
