from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update, delete
from typing import List, Optional
from datetime import datetime, timezone

from app.deps import get_async_session
from app.models.models import Servicio, Equipamiento, ServicioEquipamiento
from app.schemas.servicios import ServicioCreate, ServicioRead, ServicioUpdate
from app.schemas.equipamiento import EquipamientoRead
from app.routes.utils import not_found

router = APIRouter(prefix="/servicios", tags=["Servicios"])


@router.post("/", response_model=ServicioRead, status_code=status.HTTP_201_CREATED)
async def create_servicio(
    servicio: ServicioCreate, session: AsyncSession = Depends(get_async_session)
):
    """Crear un nuevo servicio (requiere al menos un equipamiento asignado)"""
    # Verificar que los equipamientos existen
    if not servicio.equipamiento_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Se requiere al menos un equipamiento asignado al servicio",
        )

    for equip_id in servicio.equipamiento_ids:
        equip_query = select(Equipamiento).where(Equipamiento.id == equip_id)
        equip_result = await session.execute(equip_query)
        equipamiento = equip_result.scalar_one_or_none()

        if not equipamiento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Equipamiento con ID {equip_id} no encontrado",
            )

    # Crear el servicio
    now = datetime.now(timezone.utc)
    servicio_data = servicio.dict(exclude={"equipamiento_ids"})
    nuevo_servicio = Servicio(**servicio_data, created_at=now, updated_at=now)

    session.add(nuevo_servicio)
    await session.commit()
    await session.refresh(nuevo_servicio)

    # Crear relaciones con equipamientos
    for equip_id in servicio.equipamiento_ids:
        # Verificar que `nuevo_servicio.id` no sea None antes de usarlo
        if nuevo_servicio.id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El servicio no tiene un ID válido",
            )

        # Crear la relación solo si el ID es válido
        relacion = ServicioEquipamiento(
            servicio_id=nuevo_servicio.id, equipamiento_id=equip_id, created_at=now  # type: ignore
        )
        session.add(relacion)

    await session.commit()
    await session.refresh(nuevo_servicio)

    return nuevo_servicio


@router.get("/", response_model=List[ServicioRead])
async def read_all_servicios(
    offset: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session),
):
    """Obtener lista paginada de servicios"""
    query = select(Servicio).offset(offset).limit(limit)
    result = await session.execute(query)
    servicios = result.scalars().all()
    return servicios


@router.get("/{servicio_id}", response_model=ServicioRead)
async def read_servicio(
    servicio_id: int, session: AsyncSession = Depends(get_async_session)
):
    """Obtener un servicio por su ID"""
    query = select(Servicio).where(Servicio.id == servicio_id)
    result = await session.execute(query)
    servicio = result.scalar_one_or_none()

    if not servicio:
        not_found("Servicio")
        return  # Add return to satisfy type checker, though not_found raises HTTPException

    return servicio


@router.put("/{servicio_id}", response_model=ServicioRead)
async def update_servicio(
    servicio_id: int,
    servicio_update: ServicioUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Actualizar un servicio"""
    query = select(Servicio).where(Servicio.id == servicio_id)
    result = await session.execute(query)
    servicio = result.scalar_one_or_none()

    if not servicio:
        not_found("Servicio")
        return  # Add return to satisfy type checker, though not_found raises HTTPException

    # Actualizar los campos básicos
    servicio_data = servicio_update.dict(
        exclude={"equipamiento_ids"}, exclude_unset=False, exclude_none=True
    )
    for key, value in servicio_data.items():
        setattr(servicio, key, value)

    servicio.updated_at = datetime.now(timezone.utc)

    # Si se proporciona equipamiento_ids, reemplazar el conjunto de equipamiento
    if servicio_update.equipamiento_ids is not None:
        # Verificar que los nuevos equipamientos existen
        for equip_id in servicio_update.equipamiento_ids:
            equip_query = select(Equipamiento).where(Equipamiento.id == equip_id)
            equip_result = await session.execute(equip_query)
            equipamiento = equip_result.scalar_one_or_none()

            if not equipamiento:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Equipamiento con ID {equip_id} no encontrado",
                )

        # Eliminar todas las relaciones existentes
        delete_query = delete(ServicioEquipamiento).where(
            ServicioEquipamiento.servicio_id == servicio_id  # type: ignore
        )
        await session.execute(delete_query)

        # Crear nuevas relaciones
        now = datetime.now(timezone.utc)
        for equip_id in servicio_update.equipamiento_ids:
            relacion = ServicioEquipamiento(
                servicio_id=servicio_id, equipamiento_id=equip_id, created_at=now
            )
            session.add(relacion)

    await session.commit()
    await session.refresh(servicio)

    return servicio


@router.patch("/{servicio_id}", response_model=ServicioRead)
async def partial_update_servicio(
    servicio_id: int,
    servicio_update: ServicioUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Actualizar parcialmente un servicio"""
    query = select(Servicio).where(Servicio.id == servicio_id)
    result = await session.execute(query)
    servicio = result.scalar_one_or_none()

    if not servicio:
        not_found("Servicio")
        return  # Add return to satisfy type checker, though not_found raises HTTPException

    # Actualizar solo los campos proporcionados
    servicio_data = servicio_update.dict(
        exclude={"equipamiento_ids"}, exclude_unset=True, exclude_none=True
    )
    for key, value in servicio_data.items():
        setattr(servicio, key, value)

    servicio.updated_at = datetime.now(timezone.utc)

    # Si se proporciona equipamiento_ids, reemplazar el conjunto de equipamiento
    if servicio_update.equipamiento_ids is not None:
        # Verificar que los nuevos equipamientos existen
        for equip_id in servicio_update.equipamiento_ids:
            equip_query = select(Equipamiento).where(Equipamiento.id == equip_id)
            equip_result = await session.execute(equip_query)
            equipamiento = equip_result.scalar_one_or_none()

            if not equipamiento:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Equipamiento con ID {equip_id} no encontrado",
                )

        # Eliminar todas las relaciones existentes
        delete_query = delete(ServicioEquipamiento).where(
            ServicioEquipamiento.servicio_id == servicio_id  # type: ignore
        )
        await session.execute(delete_query)

        # Crear nuevas relaciones
        now = datetime.now(timezone.utc)
        for equip_id in servicio_update.equipamiento_ids:
            relacion = ServicioEquipamiento(
                servicio_id=servicio_id, equipamiento_id=equip_id, created_at=now
            )
            session.add(relacion)

    await session.commit()
    await session.refresh(servicio)

    return servicio


@router.delete("/{servicio_id}", response_model=ServicioRead)
async def delete_servicio(
    servicio_id: int, session: AsyncSession = Depends(get_async_session)
):
    """Eliminar un servicio"""
    query = select(Servicio).where(Servicio.id == servicio_id)
    result = await session.execute(query)
    servicio = result.scalar_one_or_none()

    if not servicio:
        not_found("Servicio")
        return  # Add return to satisfy type checker, though not_found raises HTTPException

    # Eliminar relaciones en tabla pivote
    delete_query = delete(ServicioEquipamiento).where(
        ServicioEquipamiento.servicio_id == servicio_id  # type: ignore
    )
    await session.execute(delete_query)

    # Eliminar el servicio
    await session.delete(servicio)
    await session.commit()

    return servicio


@router.get("/{servicio_id}/equipamiento", response_model=List[EquipamientoRead])
async def read_servicio_equipamiento(
    servicio_id: int, session: AsyncSession = Depends(get_async_session)
):
    """Obtener equipamiento vinculado a un servicio"""
    # Verificar que el servicio existe
    servicio_query = select(Servicio).where(Servicio.id == servicio_id)
    servicio_result = await session.execute(servicio_query)
    db_servicio = servicio_result.scalar_one_or_none()

    if not db_servicio:
        not_found("Servicio")
        return []

    # 1. Get ServicioEquipamiento links
    links_query = select(ServicioEquipamiento).where(
        ServicioEquipamiento.servicio_id == db_servicio.id
    )  # Use db_servicio.id
    links_result = await session.execute(links_query)
    servicio_equipamiento_links = links_result.scalars().all()

    if not servicio_equipamiento_links:
        return []

    # 2. Get equipamiento_ids
    equipamiento_ids = [
        link.equipamiento_id
        for link in servicio_equipamiento_links
        if link.equipamiento_id is not None
    ]

    if not equipamiento_ids:
        return []

    # 3. Fetch Equipamiento objects
    # Correct usage of in_ operator with SQLModel/SQLAlchemy
    equipos_query = select(Equipamiento).where(
        getattr(Equipamiento.id, "in_")(equipamiento_ids)
    )
    equipos_result = await session.execute(equipos_query)
    equipamientos = equipos_result.scalars().all()

    return equipamientos


@router.get(
    "/equipamiento/{equipamiento_id}/servicios", response_model=List[ServicioRead]
)
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
        return []  # Return empty list or raise error

    # Obtener servicios relacionados
    # Correct join condition for SQLAlchemy/SQLModel
    # 1. Get ServicioEquipamiento links for the given equipamiento_id
    links_query = select(ServicioEquipamiento).where(
        ServicioEquipamiento.equipamiento_id == equipamiento_id
    )
    links_result = await session.execute(links_query)
    servicio_equipamiento_links = links_result.scalars().all()

    if not servicio_equipamiento_links:
        return []

    # 2. Get servicio_ids
    servicio_ids = [
        link.servicio_id
        for link in servicio_equipamiento_links
        if link.servicio_id is not None
    ]

    if not servicio_ids:
        return []

    # 3. Fetch Servicio objects
    servicios_query = select(Servicio).where(getattr(Servicio.id, "in_")(servicio_ids))
    servicios_result = await session.execute(servicios_query)
    servicios = servicios_result.scalars().all()

    return servicios
