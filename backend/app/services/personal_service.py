from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Personal, PersonalProyecto, Proyecto


# CREATE
async def crear_personal(db: AsyncSession, data: Dict[str, Any]) -> Personal:
    # Verificar que el email es único si está presente
    if "email" in data and data["email"]:
        email_query = select(Personal).where(Personal.email == data["email"])
        email_result = await db.execute(email_query)
        existing_personal = email_result.scalar_one_or_none()

        if existing_personal:
            raise ValueError(f"Ya existe un personal con el email {data['email']}")

    now = datetime.now(timezone.utc)
    obj = Personal(**data, created_at=now, updated_at=now)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


# READ ALL
async def listar_personal(
    db: AsyncSession, offset: int = 0, limit: int = 100
) -> List[Personal]:
    query = select(Personal).offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


# READ ONE
async def obtener_personal(db: AsyncSession, pid: int) -> Optional[Personal]:
    query = select(Personal).where(Personal.id == pid)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# UPDATE
async def actualizar_personal(
    db: AsyncSession, pid: int, data: Dict[str, Any], partial: bool = False
) -> Optional[Personal]:
    personal = await obtener_personal(db, pid)

    if not personal:
        return None

    # Filter data based on whether it's a partial update
    update_data = {k: v for k, v in data.items() if not partial or v is not None}

    # Update fields
    for key, value in update_data.items():
        setattr(personal, key, value)

    personal.updated_at = datetime.now(timezone.utc)
    db.add(personal)
    await db.commit()
    await db.refresh(personal)
    return personal


# DELETE (soft delete)
async def borrar_personal(db: AsyncSession, pid: int) -> Optional[Personal]:
    personal = await obtener_personal(db, pid)

    if not personal:
        return None

    # Soft delete: establecer fecha_baja
    personal.fecha_baja = datetime.now(timezone.utc).date()
    personal.updated_at = datetime.now(timezone.utc)

    # Remove relationships in pivot table
    pivot_query = select(PersonalProyecto).where(PersonalProyecto.personal_id == pid)
    pivot_result = await db.execute(pivot_query)
    pivot_records = pivot_result.scalars().all()

    for record in pivot_records:
        await db.delete(record)

    await db.commit()
    await db.refresh(personal)
    return personal


# LIST PROJECTS
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
    return result.scalars().all()


# LINK PROJECTS
async def vincular_proyectos(
    db: AsyncSession, pid: int, items: List[Dict[str, Any]]
) -> List[PersonalProyecto]:
    # Check if personal exists
    personal = await obtener_personal(db, pid)
    if not personal:
        raise ValueError(f"Personal with ID {pid} not found")

    # Create records in pivot table
    now = datetime.now(timezone.utc)
    created_relations = []

    for item in items:
        proyecto_id = item.get("proyecto_id")
        if proyecto_id is None:
            raise ValueError("Cada item debe tener un proyecto_id")

        rol = item.get("rol", "Investigador")

        # Validate project exists
        proyecto_query = select(Proyecto).where(Proyecto.id == proyecto_id)
        proyecto_result = await db.execute(proyecto_query)
        proyecto = proyecto_result.scalar_one_or_none()

        if not proyecto:
            raise ValueError(f"Project with ID {proyecto_id} not found")

        # Check if relation already exists
        relation_query = select(PersonalProyecto).where(
            PersonalProyecto.personal_id == pid,
            PersonalProyecto.proyecto_id == proyecto_id,
        )
        relation_result = await db.execute(relation_query)
        existing_relation = relation_result.scalar_one_or_none()

        if existing_relation:
            # Update role if different
            if existing_relation.rol != rol:
                existing_relation.rol = rol
                db.add(existing_relation)
                created_relations.append(existing_relation)
        else:
            # Create new relation
            new_relation = PersonalProyecto(
                personal_id=pid, proyecto_id=proyecto_id, rol=rol, created_at=now
            )
            db.add(new_relation)
            created_relations.append(new_relation)

    await db.commit()

    # Refresh created relations
    for relation in created_relations:
        await db.refresh(relation)

    # Return all relations for this personal
    return await listar_proyectos_personal(db, pid)
