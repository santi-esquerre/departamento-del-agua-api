from datetime import datetime, timezone
from typing import List, Optional, Sequence, Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Publicacion, Personal


# CREATE
async def crear_publicacion(db: AsyncSession, data: Dict[str, Any]) -> Publicacion:
    now = datetime.now(timezone.utc)

    # Validar que los personal_id en authors existan
    authors_data = data.get("authors", "[]")
    if isinstance(authors_data, str):
        import json

        try:
            authors = json.loads(authors_data)
        except json.JSONDecodeError:
            authors = []
    else:
        authors = authors_data

    # Validar que los personal_id en authors existan
    if authors and isinstance(authors, list):
        for author in authors:
            if isinstance(author, dict) and "personal_id" in author:
                personal_id = author["personal_id"]
                personal = await db.execute(
                    select(Personal).where(Personal.id == personal_id)
                )
                if not personal.scalar_one_or_none():
                    raise ValueError(f"Personal with ID {personal_id} not found")

    obj = Publicacion(**data, created_at=now, updated_at=now)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


# READ ALL
async def listar_publicaciones(
    db: AsyncSession,
    offset: int = 0,
    limit: int = 100,
    anio: Optional[int] = None,
    estado: Optional[str] = None,
) -> List[Publicacion]:
    query = select(Publicacion)

    # Aplicar filtros si están definidos
    if anio is not None:
        query = query.where(Publicacion.anio == anio)
    if estado:
        query = query.where(Publicacion.estado == estado)

    # Paginación
    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


# READ ONE
async def obtener_publicacion(db: AsyncSession, pid: int) -> Optional[Publicacion]:
    query = select(Publicacion).where(Publicacion.id == pid)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# UPDATE
async def actualizar_publicacion(
    db: AsyncSession, pid: int, data: Dict[str, Any]
) -> Optional[Publicacion]:
    publicacion = await obtener_publicacion(db, pid)

    if not publicacion:
        return None

    # Validar que los personal_id en authors existan
    if "authors" in data:
        authors_data = data.get("authors", "[]")
        if isinstance(authors_data, str):
            import json

            try:
                authors = json.loads(authors_data)
            except json.JSONDecodeError:
                authors = []
        else:
            authors = authors_data

        if authors and isinstance(authors, list):
            for author in authors:
                if isinstance(author, dict) and "personal_id" in author:
                    personal_id = author["personal_id"]
                    personal = await db.execute(
                        select(Personal).where(Personal.id == personal_id)
                    )
                    if not personal.scalar_one_or_none():
                        raise ValueError(f"Personal with ID {personal_id} not found")

    # Actualizar campos
    for key, value in data.items():
        setattr(publicacion, key, value)

    publicacion.updated_at = datetime.now(timezone.utc)
    db.add(publicacion)
    await db.commit()
    await db.refresh(publicacion)
    return publicacion


# DELETE
async def borrar_publicacion(db: AsyncSession, pid: int) -> None:
    publicacion = await obtener_publicacion(db, pid)

    if not publicacion:
        return

    await db.delete(publicacion)
    await db.commit()
