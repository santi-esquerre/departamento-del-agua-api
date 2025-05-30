from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.deps import get_async_session
from app.services import personal_service as svc
from app.schemas.personal import (
    PersonalCreate,
    PersonalRead,
    PersonalUpdate,
    PersonalProyectoRead,
    PersonalProyectoCreate,
)
from app.routes.utils import not_found

router = APIRouter(prefix="/personal", tags=["Personal"])


@router.post("/", response_model=PersonalRead, status_code=status.HTTP_201_CREATED)
async def create_personal(
    personal: PersonalCreate, db: AsyncSession = Depends(get_async_session)
):
    """Crear un nuevo registro de personal"""
    try:
        return await svc.crear_personal(db, personal.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[PersonalRead])
async def read_all_personal(
    offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)
):
    """Obtener lista paginada de personal"""
    return await svc.listar_personal(db, offset, limit)


@router.get("/{personal_id}", response_model=PersonalRead)
async def read_personal(
    personal_id: int, db: AsyncSession = Depends(get_async_session)
):
    """Obtener un registro de personal por su ID"""
    personal = await svc.obtener_personal(db, personal_id)

    if not personal:
        not_found("Personal")

    return personal


@router.put("/{personal_id}", response_model=PersonalRead)
async def update_personal(
    personal_id: int,
    personal_update: PersonalUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """Actualizar un registro de personal"""
    try:
        personal = await svc.actualizar_personal(
            db,
            personal_id,
            personal_update.model_dump(exclude_unset=False, exclude_none=True),
            partial=False,
        )

        if not personal:
            not_found("Personal")

        return personal
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{personal_id}", response_model=PersonalRead)
async def partial_update_personal(
    personal_id: int,
    personal_update: PersonalUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """Actualizar parcialmente un registro de personal"""
    try:
        personal = await svc.actualizar_personal(
            db,
            personal_id,
            personal_update.model_dump(exclude_unset=True, exclude_none=True),
            partial=True,
        )

        if not personal:
            not_found("Personal")

        return personal
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{personal_id}", response_model=PersonalRead)
async def delete_personal(
    personal_id: int, db: AsyncSession = Depends(get_async_session)
):
    """Realizar soft delete de un registro de personal"""
    personal = await svc.borrar_personal(db, personal_id)

    if not personal:
        not_found("Personal")

    return personal


@router.get("/{personal_id}/proyectos", response_model=List[PersonalProyectoRead])
async def read_personal_proyectos(
    personal_id: int, db: AsyncSession = Depends(get_async_session)
):
    """Obtener proyectos vinculados a un personal"""
    # Verificar que el personal existe
    personal = await svc.obtener_personal(db, personal_id)

    if not personal:
        not_found("Personal")

    return await svc.listar_proyectos_personal(db, personal_id)


@router.post(
    "/{personal_id}/proyectos",
    response_model=List[PersonalProyectoRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_personal_proyectos(
    personal_id: int,
    personal_proyectos: List[PersonalProyectoCreate],
    db: AsyncSession = Depends(get_async_session),
):
    """Vincular proyectos a un personal"""
    try:
        return await svc.vincular_proyectos(
            db, personal_id, [item.model_dump() for item in personal_proyectos]
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
