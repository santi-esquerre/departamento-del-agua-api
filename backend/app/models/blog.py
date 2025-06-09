# app/models/blog.py

from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Boolean, Column


class BlogPost(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    contenido: str
    resumen: Optional[str] = None
    imagen_url: Optional[str] = None
    autor: Optional[str] = None
    fecha_publicacion: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    tags: Optional[str] = None  # Comma-separated tags
    publicado: bool = Field(default=True, sa_column=Column(Boolean))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
