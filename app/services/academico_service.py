# app/services/academico_service.py

from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.academico import Carrera, Materia, Requisito, TipoRequisito


# Carrera Services
async def crear_carrera(db: AsyncSession, data: Dict[str, Any]) -> Carrera:
    now = datetime.now(timezone.utc)
    obj = Carrera(**data, created_at=now, updated_at=now)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def listar_carreras(
    db: AsyncSession, offset: int = 0, limit: int = 100
) -> List[Carrera]:
    query = select(Carrera).offset(offset).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def obtener_carrera(db: AsyncSession, cid: int) -> Optional[Carrera]:
    query = select(Carrera).where(Carrera.id == cid)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def actualizar_carrera(
    db: AsyncSession, cid: int, data: Dict[str, Any]
) -> Optional[Carrera]:
    carrera = await obtener_carrera(db, cid)

    if not carrera:
        return None

    # Update fields
    for key, value in data.items():
        setattr(carrera, key, value)

    carrera.updated_at = datetime.now(timezone.utc)
    db.add(carrera)
    await db.commit()
    await db.refresh(carrera)
    return carrera


async def borrar_carrera(db: AsyncSession, cid: int) -> Optional[Carrera]:
    carrera = await obtener_carrera(db, cid)

    if not carrera:
        return None

    await db.delete(carrera)
    await db.commit()
    return carrera


# Materia Services
async def crear_materia(db: AsyncSession, data: Dict[str, Any]) -> Materia:
    # Verificar que la carrera existe
    carrera_id = data.get("id_carrera")
    if carrera_id:
        carrera_query = select(Carrera).where(Carrera.id == carrera_id)
        carrera_result = await db.execute(carrera_query)
        carrera = carrera_result.scalar_one_or_none()

        if not carrera:
            raise ValueError(f"Carrera con ID {carrera_id} no encontrada")

    now = datetime.now(timezone.utc)
    obj = Materia(**data, created_at=now, updated_at=now)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def listar_materias(
    db: AsyncSession,
    offset: int = 0,
    limit: int = 100,
    carrera_id: Optional[int] = None,
) -> List[Materia]:
    if carrera_id:
        query = (
            select(Materia)
            .where(Materia.id_carrera == carrera_id)
            .offset(offset)
            .limit(limit)
        )
    else:
        query = select(Materia).offset(offset).limit(limit)

    result = await db.execute(query)
    return list(result.scalars().all())


async def obtener_materia(db: AsyncSession, mid: int) -> Optional[Materia]:
    query = select(Materia).where(Materia.id == mid)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def actualizar_materia(
    db: AsyncSession, mid: int, data: Dict[str, Any]
) -> Optional[Materia]:
    materia = await obtener_materia(db, mid)

    if not materia:
        return None

    # Verificar que la carrera existe si se va a actualizar
    if "id_carrera" in data and data["id_carrera"]:
        carrera_query = select(Carrera).where(Carrera.id == data["id_carrera"])
        carrera_result = await db.execute(carrera_query)
        carrera = carrera_result.scalar_one_or_none()

        if not carrera:
            raise ValueError(f"Carrera con ID {data['id_carrera']} no encontrada")

    # Update fields
    for key, value in data.items():
        setattr(materia, key, value)

    materia.updated_at = datetime.now(timezone.utc)
    db.add(materia)
    await db.commit()
    await db.refresh(materia)
    return materia


async def borrar_materia(db: AsyncSession, mid: int) -> Optional[Materia]:
    materia = await obtener_materia(db, mid)

    if not materia:
        return None

    # Eliminar los requisitos asociados
    requisitos_query = select(Requisito).where(
        (Requisito.id_materia == mid) | (Requisito.id_materia_requisito == mid)
    )
    requisitos_result = await db.execute(requisitos_query)
    requisitos = requisitos_result.scalars().all()

    for requisito in requisitos:
        await db.delete(requisito)

    await db.delete(materia)
    await db.commit()
    return materia


# Requisito Services
async def crear_requisito(db: AsyncSession, data: Dict[str, Any]) -> Requisito:
    # Verificar que ambas materias existen
    materia_id = data.get("id_materia")
    materia_req_id = data.get("id_materia_requisito")

    if materia_id == materia_req_id:
        raise ValueError("Una materia no puede ser requisito de sí misma")

    materia_query = select(Materia).where(Materia.id == materia_id)
    materia_result = await db.execute(materia_query)
    materia = materia_result.scalar_one_or_none()

    if not materia:
        raise ValueError(f"Materia con ID {materia_id} no encontrada")

    materia_req_query = select(Materia).where(Materia.id == materia_req_id)
    materia_req_result = await db.execute(materia_req_query)
    materia_req = materia_req_result.scalar_one_or_none()

    if not materia_req:
        raise ValueError(f"Materia requisito con ID {materia_req_id} no encontrada")

    # Verificar que no exista ya el mismo requisito
    requisito_query = select(Requisito).where(
        (Requisito.id_materia == materia_id)
        & (Requisito.id_materia_requisito == materia_req_id)
    )
    requisito_result = await db.execute(requisito_query)
    requisito_existente = requisito_result.scalar_one_or_none()

    if requisito_existente:
        raise ValueError("Ya existe este requisito")

    now = datetime.now(timezone.utc)
    obj = Requisito(**data, created_at=now, updated_at=now)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def listar_requisitos(
    db: AsyncSession, materia_id: Optional[int] = None
) -> List[Requisito]:
    if materia_id:
        query = select(Requisito).where(Requisito.id_materia == materia_id)
    else:
        query = select(Requisito)

    result = await db.execute(query)
    return list(result.scalars().all())


async def obtener_requisito(db: AsyncSession, rid: int) -> Optional[Requisito]:
    query = select(Requisito).where(Requisito.id == rid)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def actualizar_requisito(
    db: AsyncSession, rid: int, data: Dict[str, Any]
) -> Optional[Requisito]:
    requisito = await obtener_requisito(db, rid)

    if not requisito:
        return None

    # Si se están actualizando las materias, verificar que existan
    if "id_materia" in data:
        materia_query = select(Materia).where(Materia.id == data["id_materia"])
        materia_result = await db.execute(materia_query)
        materia = materia_result.scalar_one_or_none()

        if not materia:
            raise ValueError(f"Materia con ID {data['id_materia']} no encontrada")

    if "id_materia_requisito" in data:
        materia_req_query = select(Materia).where(
            Materia.id == data["id_materia_requisito"]
        )
        materia_req_result = await db.execute(materia_req_query)
        materia_req = materia_req_result.scalar_one_or_none()

        if not materia_req:
            raise ValueError(
                f"Materia requisito con ID {data['id_materia_requisito']} no encontrada"
            )

    # Verificar que una materia no sea requisito de sí misma
    materia_id = data.get("id_materia", requisito.id_materia)
    materia_req_id = data.get("id_materia_requisito", requisito.id_materia_requisito)

    if materia_id == materia_req_id:
        raise ValueError("Una materia no puede ser requisito de sí misma")

    # Update fields
    for key, value in data.items():
        setattr(requisito, key, value)

    requisito.updated_at = datetime.now(timezone.utc)
    db.add(requisito)
    await db.commit()
    await db.refresh(requisito)
    return requisito


async def borrar_requisito(db: AsyncSession, rid: int) -> Optional[Requisito]:
    requisito = await obtener_requisito(db, rid)

    if not requisito:
        return None

    await db.delete(requisito)
    await db.commit()
    return requisito
