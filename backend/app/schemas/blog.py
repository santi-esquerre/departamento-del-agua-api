# app/schemas/blog.py

from datetime import datetime
from typing import List, Optional
from pydantic import ConfigDict, BaseModel, Field, validator


# BlogPost Schemas
class BlogPostBase(BaseModel):
    titulo: str
    contenido: str
    resumen: Optional[str] = None
    imagen_url: Optional[str] = None
    autor: Optional[str] = None
    tags: Optional[str] = None  # Comma-separated tags
    publicado: bool = True


class BlogPostCreate(BlogPostBase):
    pass


class BlogPostRead(BlogPostBase):
    id: int
    fecha_publicacion: datetime
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class BlogPostUpdate(BaseModel):
    titulo: Optional[str] = None
    contenido: Optional[str] = None
    resumen: Optional[str] = None
    imagen_url: Optional[str] = None
    autor: Optional[str] = None
    tags: Optional[str] = None
    publicado: Optional[bool] = None
