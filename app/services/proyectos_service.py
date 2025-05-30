from datetime import datetime, timezone
from typing import List, Optional, Sequence, Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Proyecto, PersonalProyecto, Personal
from app.services.personal_service import obtener_personal


# CREATE
async def crear_proyecto(db: AsyncSession, data: Dict[str, Any]) -> Proyecto:
    now = datetime.now(timezone.utc)

    # Validar que fecha_inicio <= fecha_fin
    if data.get("fecha_inicio") and data.get("fecha_fin"):
        if data["fecha_inicio"] > data["fecha_fin"]:
            raise ValueError(
                "La fecha de inicio debe ser anterior o igual a la fecha de fin"
            )

    obj = Proyecto(**data, created_at=now, updated_at=now)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    # Patch tzinfo if missing (SQLite)
    if obj.created_at.tzinfo is None:
        obj.created_at = obj.created_at.replace(tzinfo=timezone.utc)
    if obj.updated_at.tzinfo is None:
        obj.updated_at = obj.updated_at.replace(tzinfo=timezone.utc)
    return obj


# READ ALL
async def listar_proyectos(
    db: AsyncSession, offset: int = 0, limit: int = 100
) -> List[Proyecto]:
    query = select(Proyecto).offset(offset).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


# READ ONE
async def obtener_proyecto(db: AsyncSession, pid: int) -> Optional[Proyecto]:
    query = select(Proyecto).where(Proyecto.id == pid)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# UPDATE
async def actualizar_proyecto(
    db: AsyncSession, pid: int, data: Dict[str, Any]
) -> Optional[Proyecto]:
    proyecto = await obtener_proyecto(db, pid)

    if not proyecto:
        return None

    # Validar que fecha_inicio <= fecha_fin
    fecha_inicio = data.get("fecha_inicio", proyecto.fecha_inicio)
    fecha_fin = data.get("fecha_fin", proyecto.fecha_fin)

    if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
        raise ValueError(
            "La fecha de inicio debe ser anterior o igual a la fecha de fin"
        )

    # Actualizar campos
    for key, value in data.items():
        setattr(proyecto, key, value)

    proyecto.updated_at = datetime.now(timezone.utc)
    db.add(proyecto)
    await db.commit()
    await db.refresh(proyecto)
    # Patch tzinfo if missing (SQLite)
    if proyecto.updated_at.tzinfo is None:
        proyecto.updated_at = proyecto.updated_at.replace(tzinfo=timezone.utc)
    if proyecto.created_at.tzinfo is None:
        proyecto.created_at = proyecto.created_at.replace(tzinfo=timezone.utc)
    return proyecto


# DELETE
async def borrar_proyecto(db: AsyncSession, pid: int) -> None:
    proyecto = await obtener_proyecto(db, pid)

    if not proyecto:
        return

    # Eliminar relaciones con personal
    pivot_query = select(PersonalProyecto).where(PersonalProyecto.proyecto_id == pid)
    pivot_result = await db.execute(pivot_query)
    pivot_records = pivot_result.scalars().all()

    for record in pivot_records:
        await db.delete(record)

    await db.delete(proyecto)
    await db.commit()


# ASIGNAR PERSONAL
async def asignar_personal(
    db: AsyncSession, proyecto_id: int, personal_data: List[Dict[str, Any]]
) -> List[PersonalProyecto]:
    # Verificar que el proyecto existe
    proyecto = await obtener_proyecto(db, proyecto_id)
    if not proyecto:
        raise ValueError(f"Proyecto with ID {proyecto_id} not found")

    # Crear relaciones en la tabla pivote
    now = datetime.now(timezone.utc)
    created_relations = []

    for item in personal_data:
        personal_id = item.get("personal_id")
        if personal_id is None:
            raise ValueError("Cada item debe tener un personal_id")
        rol = item.get("rol", "Investigador")

        # Verificar que el personal existe
        personal_query = select(Personal).where(Personal.id == personal_id)
        personal_result = await db.execute(personal_query)
        personal = personal_result.scalar_one_or_none()

        if not personal:
            raise ValueError(f"Personal with ID {personal_id} not found")

        # Verificar si la relación ya existe
        relation_query = select(PersonalProyecto).where(
            PersonalProyecto.personal_id == personal_id,
            PersonalProyecto.proyecto_id == proyecto_id,
        )
        relation_result = await db.execute(relation_query)
        existing_relation = relation_result.scalar_one_or_none()

        if existing_relation:
            # Actualizar el rol si es diferente
            if existing_relation.rol != rol:
                existing_relation.rol = rol
                db.add(existing_relation)
                created_relations.append(existing_relation)
        else:
            # Crear nueva relación
            new_relation = PersonalProyecto(
                personal_id=personal_id,
                proyecto_id=proyecto_id,
                rol=rol,
                created_at=now,
            )
            db.add(new_relation)
            created_relations.append(new_relation)

    await db.commit()

    # Refrescar las relaciones creadas/actualizadas
    for relation in created_relations:
        await db.refresh(relation)

    # Retornar todas las relaciones para este proyecto
    pivot_query = select(PersonalProyecto).where(
        PersonalProyecto.proyecto_id == proyecto_id
    )
    pivot_result = await db.execute(pivot_query)
    return list(pivot_result.scalars().all())


# LISTAR PERSONAL DEL PROYECTO
async def listar_personal_proyecto(
    db: AsyncSession, proyecto_id: int
) -> List[PersonalProyecto]:
    # Verificar que el proyecto existe
    proyecto = await obtener_proyecto(db, proyecto_id)
    if not proyecto:
        return []

    # Obtener relaciones
    query = select(PersonalProyecto).where(PersonalProyecto.proyecto_id == proyecto_id)
    result = await db.execute(query)
    return list(result.scalars().all())


# LISTAR PROYECTOS DEL PERSONAL
async def listar_proyectos_personal(
    db: AsyncSession, pid: int
) -> List[PersonalProyecto]:
    # Check if personal exists
    personal = await obtener_personal(db, pid)
    if not personal:
        return []
    # Get related projects
    query = select(PersonalProyecto).where(PersonalProyecto.personal_id == pid)
    result = await db.execute(query)
    return list(result.scalars().all())
