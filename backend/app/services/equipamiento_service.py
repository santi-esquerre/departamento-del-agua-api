from datetime import datetime, timezone
from typing import List, Optional, Sequence, Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Equipamiento, EquipamientoActividad, ServicioEquipamiento


# CREATE
async def crear_equipamiento(db: AsyncSession, data: Dict[str, Any]) -> Equipamiento:
    now = datetime.now(timezone.utc)
    obj = Equipamiento(**data, created_at=now, updated_at=now)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


# READ ALL
async def listar_equipamientos(
    db: AsyncSession, offset: int = 0, limit: int = 100
) -> List[Equipamiento]:
    query = select(Equipamiento).offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


# READ ONE
async def obtener_equipamiento(db: AsyncSession, eid: int) -> Optional[Equipamiento]:
    query = select(Equipamiento).where(Equipamiento.id == eid)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# UPDATE
async def actualizar_equipamiento(
    db: AsyncSession, eid: int, data: Dict[str, Any]
) -> Optional[Equipamiento]:
    equipamiento = await obtener_equipamiento(db, eid)

    if not equipamiento:
        return None

    # Actualizar campos
    for key, value in data.items():
        setattr(equipamiento, key, value)

    equipamiento.updated_at = datetime.now(timezone.utc)
    db.add(equipamiento)
    await db.commit()
    await db.refresh(equipamiento)
    return equipamiento


# DELETE
async def borrar_equipamiento(db: AsyncSession, eid: int) -> None:
    equipamiento = await obtener_equipamiento(db, eid)

    if not equipamiento:
        return

    # Verificar si el equipamiento está asociado a actividades o servicios
    actividades_query = select(EquipamientoActividad).where(
        EquipamientoActividad.equipamiento_id == eid
    )
    actividades_result = await db.execute(actividades_query)
    actividades = actividades_result.scalars().all()

    servicios_query = select(ServicioEquipamiento).where(
        ServicioEquipamiento.equipamiento_id == eid
    )
    servicios_result = await db.execute(servicios_query)
    servicios = servicios_result.scalars().all()

    if actividades or servicios:
        raise ValueError(
            "No se puede eliminar el equipamiento porque está asociado a actividades o servicios"
        )

    await db.delete(equipamiento)
    await db.commit()


# ASIGNAR SERVICIO
async def asignar_servicio(
    db: AsyncSession, eid: int, servicio_id: int
) -> ServicioEquipamiento:
    # Verificar que el equipamiento existe
    equipamiento = await obtener_equipamiento(db, eid)
    if not equipamiento:
        raise ValueError(f"Equipamiento with ID {eid} not found")

    # Verificar que el servicio existe
    from app.services.servicios_service import obtener_servicio

    servicio = await obtener_servicio(db, servicio_id)
    if not servicio:
        raise ValueError(f"Servicio with ID {servicio_id} not found")

    # Verificar si la relación ya existe
    relation_query = select(ServicioEquipamiento).where(
        ServicioEquipamiento.equipamiento_id == eid,
        ServicioEquipamiento.servicio_id == servicio_id,
    )
    relation_result = await db.execute(relation_query)
    existing_relation = relation_result.scalar_one_or_none()

    if existing_relation:
        return existing_relation

    # Crear nueva relación
    now = datetime.now(timezone.utc)
    new_relation = ServicioEquipamiento(
        equipamiento_id=eid, servicio_id=servicio_id, created_at=now
    )
    db.add(new_relation)
    await db.commit()
    await db.refresh(new_relation)
    return new_relation


# LISTAR SERVICIOS DEL EQUIPAMIENTO
async def listar_servicios_equipamiento(
    db: AsyncSession, eid: int
) -> List[ServicioEquipamiento]:
    # Verificar que el equipamiento existe
    equipamiento = await obtener_equipamiento(db, eid)
    if not equipamiento:
        return []

    # Obtener relaciones
    query = select(ServicioEquipamiento).where(
        ServicioEquipamiento.equipamiento_id == eid
    )
    result = await db.execute(query)
    return result.scalars().all()
