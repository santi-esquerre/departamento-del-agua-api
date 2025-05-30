from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update, delete
from typing import List, Optional
from datetime import datetime, timezone

from app.db import get_session
from app.models.models import Publicacion, Personal
from app.schemas.publicaciones import (
    PublicacionCreate,
    PublicacionRead,
    PublicacionUpdate,
    Author,
)
from app.routes.utils import not_found

router = APIRouter(prefix="/publicaciones", tags=["Publicaciones"])


async def validate_authors(authors: List[Author], session: AsyncSession):
    """Validar que los personal_id referenciados existen"""
    for author in authors:
        if author.personal_id:
            query = select(Personal).where(Personal.id == author.personal_id)
            result = await session.execute(query)
            personal = result.scalar_one_or_none()

            if not personal:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Personal con ID {author.personal_id} no encontrado",
                )


@router.post("/", response_model=PublicacionRead, status_code=status.HTTP_201_CREATED)
async def create_publicacion(
    publicacion: PublicacionCreate, session: AsyncSession = Depends(get_session)
):
    """Crear una nueva publicación"""
    # Validar que los personal_id referenciados existen
    if publicacion.authors:
        await validate_authors(publicacion.authors, session)

    now = datetime.now(timezone.utc)
    # Convertir el modelo Pydantic a diccionario y procesarlo para la BD
    publicacion_data = publicacion.dict()

    nueva_publicacion = Publicacion(
        **publicacion_data, fecha_registro=now, created_at=now, updated_at=now
    )

    session.add(nueva_publicacion)
    await session.commit()
    await session.refresh(nueva_publicacion)

    return nueva_publicacion


@router.get("/", response_model=List[PublicacionRead])
async def read_all_publicaciones(
    offset: int = 0,
    limit: int = 100,
    anio: Optional[int] = None,
    estado: Optional[str] = None,
    autor_id: Optional[int] = None,
    session: AsyncSession = Depends(get_session),
):
    """Obtener lista paginada de publicaciones con filtros opcionales"""
    query = select(Publicacion)

    # Aplicar filtros si se proporcionan
    if anio:
        query = query.where(Publicacion.anio == anio)

    if estado:
        query = query.where(Publicacion.estado == estado)

    # Filtrar por autor_id (esto requiere procesamiento adicional)
    results = await session.execute(query.offset(offset).limit(limit))
    publicaciones = results.scalars().all()

    # Si se especifició autor_id, filtrar manualmente las publicaciones
    if autor_id:
        filtered_publicaciones = []
        for pub in publicaciones:
            authors = pub.authors  # Now a list, not a JSON string
            if any(author.get("personal_id") == autor_id for author in authors):
                filtered_publicaciones.append(pub)
        return filtered_publicaciones

    return publicaciones


@router.get("/{publicacion_id}", response_model=PublicacionRead)
async def read_publicacion(
    publicacion_id: int, session: AsyncSession = Depends(get_session)
):
    """Obtener una publicación por su ID"""
    query = select(Publicacion).where(Publicacion.id == publicacion_id)
    result = await session.execute(query)
    publicacion = result.scalar_one_or_none()

    if not publicacion:
        not_found("Publicación")

    return publicacion


@router.put("/{publicacion_id}", response_model=PublicacionRead)
async def update_publicacion(
    publicacion_id: int,
    publicacion_update: PublicacionUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Actualizar una publicación completa"""
    query = select(Publicacion).where(Publicacion.id == publicacion_id)
    result = await session.execute(query)
    publicacion = result.scalar_one_or_none()

    if not publicacion:
        not_found("Publicación")
        return  # Add return to satisfy type checker, though not_found raises HTTPException

    # Validar autores si se proporcionan
    if publicacion_update.authors:
        await validate_authors(publicacion_update.authors, session)

    # Actualizar la publicación
    publicacion_data = publicacion_update.dict(exclude_unset=False, exclude_none=True)
    for key, value in publicacion_data.items():
        setattr(publicacion, key, value)

    publicacion.updated_at = datetime.now(timezone.utc)

    session.add(publicacion)
    await session.commit()
    await session.refresh(publicacion)

    return publicacion


@router.patch("/{publicacion_id}", response_model=PublicacionRead)
async def partial_update_publicacion(
    publicacion_id: int,
    publicacion_update: PublicacionUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Actualizar parcialmente una publicación"""
    query = select(Publicacion).where(Publicacion.id == publicacion_id)
    result = await session.execute(query)
    publicacion = result.scalar_one_or_none()

    if not publicacion:
        not_found("Publicación")
        return  # Add return to satisfy type checker, though not_found raises HTTPException

    # Validar autores si se proporcionan
    if publicacion_update.authors:
        await validate_authors(publicacion_update.authors, session)

    # Actualizar solo los campos proporcionados
    publicacion_data = publicacion_update.dict(exclude_unset=True, exclude_none=True)
    for key, value in publicacion_data.items():
        setattr(publicacion, key, value)

    publicacion.updated_at = datetime.now(timezone.utc)

    session.add(publicacion)
    await session.commit()
    await session.refresh(publicacion)

    return publicacion


@router.delete("/{publicacion_id}", response_model=PublicacionRead)
async def delete_publicacion(
    publicacion_id: int, session: AsyncSession = Depends(get_session)
):
    """Eliminar una publicación"""
    query = select(Publicacion).where(Publicacion.id == publicacion_id)
    result = await session.execute(query)
    publicacion = result.scalar_one_or_none()

    if not publicacion:
        not_found("Publicación")
        return  # Add return to satisfy type checker, though not_found raises HTTPException

    await session.delete(publicacion)
    await session.commit()

    # Para devolver la entidad eliminada
    return publicacion
