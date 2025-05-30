from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.deps import get_async_session
from app.services import proyectos_service as svc
from app.schemas.proyectos import (
    ProyectoCreate,
    ProyectoRead,
    ProyectoUpdate,
    ProyectoPersonalCreate,
    ProyectoPersonalRead,
)
from app.routes.utils import not_found

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])


@router.post("/", response_model=ProyectoRead, status_code=status.HTTP_201_CREATED)
async def create_proyecto(
    proyecto: ProyectoCreate, db: AsyncSession = Depends(get_async_session)
):
    """Crear un nuevo proyecto"""
    try:
        return await svc.crear_proyecto(db, proyecto.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[ProyectoRead])
async def read_all_proyectos(
    offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)
):
    """Obtener lista paginada de proyectos"""
    return await svc.listar_proyectos(db, offset, limit)


@router.get("/{proyecto_id}", response_model=ProyectoRead)
async def read_proyecto(
    proyecto_id: int, db: AsyncSession = Depends(get_async_session)
):
    """Obtener un proyecto por su ID"""
    proyecto = await svc.obtener_proyecto(db, proyecto_id)

    if not proyecto:
        not_found("Proyecto")

    return proyecto


@router.put("/{proyecto_id}", response_model=ProyectoRead)
async def update_proyecto(
    proyecto_id: int,
    proyecto_update: ProyectoUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """Actualizar un proyecto"""
    try:
        proyecto = await svc.actualizar_proyecto(
            db, proyecto_id, proyecto_update.model_dump()
        )

        if not proyecto:
            not_found("Proyecto")

        return proyecto
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{proyecto_id}")
async def delete_proyecto(
    proyecto_id: int, db: AsyncSession = Depends(get_async_session)
):
    """Eliminar un proyecto"""
    try:
        await svc.borrar_proyecto(db, proyecto_id)
        return {"message": f"Proyecto {proyecto_id} eliminado"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{proyecto_id}/personal", response_model=List[ProyectoPersonalRead])
async def read_personal_proyecto(
    proyecto_id: int, db: AsyncSession = Depends(get_async_session)
):
    """Obtener personal vinculado a un proyecto"""
    proyecto = await svc.obtener_proyecto(db, proyecto_id)

    if not proyecto:
        not_found("Proyecto")

    return await svc.listar_personal_proyecto(db, proyecto_id)


@router.post(
    "/{proyecto_id}/personal",
    response_model=List[ProyectoPersonalRead],
    status_code=status.HTTP_201_CREATED,
)
async def assign_personal(
    proyecto_id: int,
    personal_data: List[ProyectoPersonalCreate],
    db: AsyncSession = Depends(get_async_session),
):
    """Asignar personal a un proyecto"""
    try:
        return await svc.asignar_personal(
            db, proyecto_id, [item.model_dump() for item in personal_data]
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
