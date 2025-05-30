from datetime import datetime, timezone
from typing import List, Optional, Sequence, Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.models import Servicio, ServicioEquipamiento, Equipamiento


# CREATE
async def crear_servicio(
    db: AsyncSession,
    data: Dict[str, Any],
    equipamiento_ids: Optional[List[int]] = None,  # Allow None
) -> Servicio:
    now = datetime.now(timezone.utc)

    # Validar tarifa
    if data.get("tarifa") is not None and data["tarifa"] < 0:
        raise ValueError("La tarifa no puede ser negativa.")

    # Crear servicio
    obj = Servicio(**data, created_at=now, updated_at=now)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)

    # Asociar equipamientos
    if equipamiento_ids:
        for eid in equipamiento_ids:
            # Asegurarse que obj.id no es None antes de usarlo
            if obj.id is None:
                raise ValueError(
                    "ID de servicio no puede ser None al asociar equipamiento"
                )
            se = ServicioEquipamiento(
                servicio_id=obj.id, equipamiento_id=eid, created_at=now
            )
            db.add(se)
        await db.commit()  # Commit after adding all associations
    # Eagerly load equipamiento_objs (the many-to-many relationship)
    query = (
        select(Servicio)
        .options(selectinload(Servicio.equipamientos))  # type: ignore
        .where(Servicio.id == obj.id)
    )
    result = await db.execute(query)
    obj = result.scalar_one()
    return obj


# READ ALL
async def listar_servicios(
    db: AsyncSession, offset: int = 0, limit: int = 100
) -> List[Servicio]:  # Return List instead of Sequence
    query = select(Servicio).offset(offset).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())  # Convert to list


# READ ONE
async def obtener_servicio(db: AsyncSession, sid: int) -> Optional[Servicio]:
    query = select(Servicio).where(Servicio.id == sid)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# UPDATE
async def actualizar_servicio(
    db: AsyncSession, sid: int, data: Dict[str, Any]
) -> Optional[Servicio]:
    servicio = await obtener_servicio(db, sid)

    if not servicio:
        return None

    # Validar tarifa
    if data.get("tarifa") is not None and data["tarifa"] < 0:
        raise ValueError("La tarifa no puede ser negativa.")

    # Actualizar campos
    for key, value in data.items():
        setattr(servicio, key, value)

    servicio.updated_at = datetime.now(timezone.utc)
    db.add(servicio)
    await db.commit()
    await db.refresh(servicio)
    return servicio


# DELETE
async def borrar_servicio(db: AsyncSession, sid: int) -> None:
    servicio = await obtener_servicio(db, sid)

    if not servicio:
        return

    # Eliminar relaciones con equipamientos
    pivot_query = select(ServicioEquipamiento).where(
        ServicioEquipamiento.servicio_id == sid
    )
    pivot_result = await db.execute(pivot_query)
    pivot_records = pivot_result.scalars().all()

    for record in pivot_records:
        await db.delete(record)

    await db.delete(servicio)
    await db.commit()


# LISTAR EQUIPAMIENTOS DEL SERVICIO
async def listar_equipamientos_servicio(
    db: AsyncSession, sid: int
) -> List[ServicioEquipamiento]:  # Return List instead of Sequence
    query = select(ServicioEquipamiento).where(ServicioEquipamiento.servicio_id == sid)
    result = await db.execute(query)
    return list(result.scalars().all())  # Convert to list


# AGREGAR EQUIPAMIENTO A SERVICIO
async def agregar_equipamiento(
    db: AsyncSession, sid: int, eid: int
) -> ServicioEquipamiento:
    # Verificar que el servicio existe
    servicio = await obtener_servicio(db, sid)
    if not servicio:
        raise ValueError(f"Servicio with ID {sid} not found")

    # Verificar que el equipamiento existe
    from app.services.equipamiento_service import obtener_equipamiento

    equipamiento = await obtener_equipamiento(db, eid)
    if not equipamiento:
        raise ValueError(f"Equipamiento with ID {eid} not found")

    # Verificar si la relación ya existe
    relation_query = select(ServicioEquipamiento).where(
        ServicioEquipamiento.servicio_id == sid,
        ServicioEquipamiento.equipamiento_id == eid,
    )
    relation_result = await db.execute(relation_query)
    existing_relation = relation_result.scalar_one_or_none()

    if existing_relation:
        return existing_relation

    # Crear nueva relación
    now = datetime.now(timezone.utc)
    new_relation = ServicioEquipamiento(
        servicio_id=sid, equipamiento_id=eid, created_at=now
    )
    db.add(new_relation)
    await db.commit()
    await db.refresh(new_relation)
    return new_relation
