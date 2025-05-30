# app/services/blog_service.py

from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, desc, select, literal
from sqlalchemy.sql.expression import true
from app.models.blog import BlogPost


async def crear_post(db: AsyncSession, data: Dict[str, Any]) -> BlogPost:
    now = datetime.now(timezone.utc)

    # If fecha_publicacion is not specified, use current time
    if "fecha_publicacion" not in data:
        data["fecha_publicacion"] = now

    obj = BlogPost(**data, created_at=now, updated_at=now)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def listar_posts(
    db: AsyncSession,
    offset: int = 0,
    limit: int = 100,
    tag: Optional[str] = None,
    solo_publicados: bool = False,
) -> List[BlogPost]:
    query = select(BlogPost)

    if solo_publicados:
        query = query.where(BlogPost.publicado == True)  # type: ignore

    if tag:
        query = query.where(text(f"tags LIKE '%{tag}%'"))

    # For ordering, use getattr to get the column
    query = (
        query.order_by(getattr(BlogPost, "fecha_publicacion").desc())
        .offset(offset)
        .limit(limit)
    )
    result = await db.execute(query)
    return list(result.scalars().all())


async def obtener_post(db: AsyncSession, pid: int) -> Optional[BlogPost]:
    query = select(BlogPost).where(BlogPost.id == pid)  # type: ignore
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def actualizar_post(
    db: AsyncSession, pid: int, data: Dict[str, Any]
) -> Optional[BlogPost]:
    post = await obtener_post(db, pid)

    if not post:
        return None

    # Update fields
    for key, value in data.items():
        setattr(post, key, value)

    post.updated_at = datetime.now(timezone.utc)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def borrar_post(db: AsyncSession, pid: int) -> Optional[BlogPost]:
    post = await obtener_post(db, pid)

    if not post:
        return None

    await db.delete(post)
    await db.commit()
    return post


async def buscar_posts(
    db: AsyncSession,
    termino: str,
    offset: int = 0,
    limit: int = 100,
    solo_publicados: bool = False,
) -> List[BlogPost]:
    query = select(BlogPost)

    if solo_publicados:
        query = query.where(BlogPost.publicado == True)  # type: ignore

    # Buscar en título, contenido y resumen usando LIKE
    like_term = f"%{termino}%"
    query = query.where(
        text(
            f"titulo LIKE :like_term OR contenido LIKE :like_term OR resumen LIKE :like_term"
        )
    ).params(like_term=like_term)
    query = (
        query.order_by(getattr(BlogPost, "fecha_publicacion").desc())
        .offset(offset)
        .limit(limit)
    )
    result = await db.execute(query)
    return list(result.scalars().all())
