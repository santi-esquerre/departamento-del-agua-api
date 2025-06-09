from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update, delete
from typing import List, Optional
from datetime import datetime, timezone

from app.deps import get_async_session, get_current_admin
from app.models.models import (
    Equipamiento,
    Actividad,
    EquipamientoActividad,
    Servicio,
    ServicioEquipamiento,
)
from app.schemas.equipamiento import (
    EquipamientoCreate,
    EquipamientoRead,
    EquipamientoUpdate,
    EquipamientoActividadRead,
)
from app.routes.utils import not_found

router = APIRouter(prefix="/equipamiento", tags=["Equipamiento"])

ADMIN = Depends(get_current_admin)


@router.post(
    "/",
    response_model=EquipamientoRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[ADMIN],
)
async def create_equipamiento(
    equipamiento: EquipamientoCreate, session: AsyncSession = Depends(get_async_session)
):
    """Crear un nuevo equipamiento"""
    now = datetime.now(timezone.utc)
    nuevo_equipamiento = Equipamiento(
        **equipamiento.dict(), created_at=now, updated_at=now
    )
    session.add(nuevo_equipamiento)
    await session.commit()
    await session.refresh(nuevo_equipamiento)
    return nuevo_equipamiento


@router.get("/", response_model=List[EquipamientoRead])
async def read_all_equipamiento(
    offset: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session),
):
    """Obtener lista paginada de equipamiento"""
    query = select(Equipamiento).offset(offset).limit(limit)
    result = await session.execute(query)
    equipamiento_list = result.scalars().all()
    return equipamiento_list


@router.get("/{equipamiento_id}", response_model=EquipamientoRead)
async def read_equipamiento(
    equipamiento_id: int, session: AsyncSession = Depends(get_async_session)
):
    """Obtener un equipamiento por su ID"""
    query = select(Equipamiento).where(Equipamiento.id == equipamiento_id)
    result = await session.execute(query)
    equipamiento = result.scalar_one_or_none()

    if not equipamiento:
        not_found("Equipamiento")
        return  # Add return to satisfy type checker, though not_found raises HTTPException

    return equipamiento


@router.put("/{equipamiento_id}", response_model=EquipamientoRead)
async def update_equipamiento(
    equipamiento_id: int,
    equipamiento_update: EquipamientoUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Actualizar un equipamiento"""
    query = select(Equipamiento).where(Equipamiento.id == equipamiento_id)
    result = await session.execute(query)
    equipamiento = result.scalar_one_or_none()

    if not equipamiento:
        not_found("Equipamiento")
        return

    # Actualizar todos los campos
    equipamiento_data = equipamiento_update.dict(exclude_unset=False, exclude_none=True)
    for key, value in equipamiento_data.items():
        setattr(equipamiento, key, value)

    equipamiento.updated_at = datetime.now(timezone.utc)

    session.add(equipamiento)
    await session.commit()
    await session.refresh(equipamiento)

    return equipamiento


@router.patch("/{equipamiento_id}", response_model=EquipamientoRead)
async def partial_update_equipamiento(
    equipamiento_id: int,
    equipamiento_update: EquipamientoUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Actualizar parcialmente un equipamiento"""
    query = select(Equipamiento).where(Equipamiento.id == equipamiento_id)
    result = await session.execute(query)
    equipamiento = result.scalar_one_or_none()

    if not equipamiento:
        not_found("Equipamiento")
        return

    # Actualizar solo los campos proporcionados
    equipamiento_data = equipamiento_update.dict(exclude_unset=True, exclude_none=True)
    for key, value in equipamiento_data.items():
        setattr(equipamiento, key, value)

    equipamiento.updated_at = datetime.now(timezone.utc)

    session.add(equipamiento)
    await session.commit()
    await session.refresh(equipamiento)

    return equipamiento


@router.delete(
    "/{equipamiento_id}", response_model=EquipamientoRead, dependencies=[ADMIN]
)
async def delete_equipamiento(
    equipamiento_id: int, session: AsyncSession = Depends(get_async_session)
):
    """Eliminar un equipamiento"""
    query = select(Equipamiento).where(Equipamiento.id == equipamiento_id)
    result = await session.execute(query)
    equipamiento = result.scalar_one_or_none()

    if not equipamiento:
        not_found("Equipamiento")
        return

    # Verificar si el equipamiento está asociado a actividades o servicios
    actividades_query = select(EquipamientoActividad).where(
        EquipamientoActividad.equipamiento_id == equipamiento_id
    )
    actividades_result = await session.execute(actividades_query)
    actividades_count = len(actividades_result.scalars().all())

    servicios_query = select(ServicioEquipamiento).where(
        ServicioEquipamiento.equipamiento_id == equipamiento_id
    )
    servicios_result = await session.execute(servicios_query)
    servicios_count = len(servicios_result.scalars().all())

    if actividades_count > 0 or servicios_count > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"No se puede eliminar equipamiento con ID {equipamiento_id} porque está asociado a {actividades_count} actividades y {servicios_count} servicios",
        )

    await session.delete(equipamiento)
    await session.commit()

    return equipamiento


@router.get(
    "/{equipamiento_id}/actividades", response_model=List[EquipamientoActividadRead]
)
async def read_equipamiento_actividades(
    equipamiento_id: int, session: AsyncSession = Depends(get_async_session)
):
    """Obtener actividades vinculadas a un equipamiento"""
    # Verificar que el equipamiento existe
    equipamiento_query = select(Equipamiento).where(Equipamiento.id == equipamiento_id)
    equipamiento_result = await session.execute(equipamiento_query)
    equipamiento = equipamiento_result.scalar_one_or_none()

    if not equipamiento:
        not_found("Equipamiento")
        return

    # Obtener actividades relacionadas
    query = select(EquipamientoActividad).where(
        EquipamientoActividad.equipamiento_id == equipamiento_id
    )
    result = await session.execute(query)
    actividades = result.scalars().all()

    return actividades


@router.get("/{equipamiento_id}/servicios", response_model=List[dict])
async def read_equipamiento_servicios(
    equipamiento_id: int, session: AsyncSession = Depends(get_async_session)
):
    """Obtener servicios vinculados a un equipamiento"""
    # Verificar que el equipamiento existe
    equipamiento_query = select(Equipamiento).where(Equipamiento.id == equipamiento_id)
    equipamiento_result = await session.execute(equipamiento_query)
    equipamiento = equipamiento_result.scalar_one_or_none()

    if not equipamiento:
        not_found("Equipamiento")
        return

    # Obtener servicios relacionados
    servicios_query = (
        select(ServicioEquipamiento, Servicio)
        .join(Servicio, ServicioEquipamiento.servicio_id == Servicio.id)  # type: ignore
        .where(ServicioEquipamiento.equipamiento_id == equipamiento_id)
    )

    servicios_result = await session.execute(servicios_query)
    servicios_data = []

    for pivote, servicio in servicios_result:
        servicios_data.append(
            {
                "servicio_id": servicio.id,
                "nombre": servicio.nombre,
                "descripcion": servicio.descripcion,
                "created_at": pivote.created_at,
            }
        )

    return servicios_data


@router.post("/{equipamiento_id}/servicios", response_model=List[dict])
async def assign_equipamiento_servicios(
    equipamiento_id: int,
    servicio_ids: List[int],
    session: AsyncSession = Depends(get_async_session),
):
    """Asignar servicios a un equipamiento"""
    # Verificar que el equipamiento existe
    equipamiento_query = select(Equipamiento).where(Equipamiento.id == equipamiento_id)
    equipamiento_result = await session.execute(equipamiento_query)
    equipamiento = equipamiento_result.scalar_one_or_none()

    if not equipamiento:
        not_found("Equipamiento")
        return

    # Verificar que los servicios existen
    for servicio_id in servicio_ids:
        servicio_query = select(Servicio).where(Servicio.id == servicio_id)
        servicio_result = await session.execute(servicio_query)
        servicio = servicio_result.scalar_one_or_none()

        if not servicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Servicio con ID {servicio_id} no encontrado",
            )

    # Crear registros en la tabla pivote
    now = datetime.now(timezone.utc)

    for servicio_id in servicio_ids:
        # Verificar si la relación ya existe
        relation_query = select(ServicioEquipamiento).where(
            ServicioEquipamiento.equipamiento_id == equipamiento_id,
            ServicioEquipamiento.servicio_id == servicio_id,
        )
        relation_result = await session.execute(relation_query)
        existing_relation = relation_result.scalar_one_or_none()

        if not existing_relation:
            # Crear nueva relación
            new_relation = ServicioEquipamiento(
                equipamiento_id=equipamiento_id, servicio_id=servicio_id, created_at=now
            )
            session.add(new_relation)

    await session.commit()

    # Devolver todos los servicios asociados
    return await read_equipamiento_servicios(equipamiento_id, session)
