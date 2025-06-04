from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlmodel import select
from sqlalchemy import text

from app.deps import get_async_session
from app.services import blog_service as svc
from app.schemas.blog import (
    BlogPostCreate,
    BlogPostRead,
    BlogPostUpdate,
)
from app.routes.utils import not_found
from app.models.blog import BlogPost
from app.services.email_service import send_html
from app.services.subscriber_service import list_emails
from fastapi import Depends
from app.deps import get_current_admin

ADMIN = Depends(get_current_admin)

router = APIRouter(prefix="/blog", tags=["Blog"])


@router.post(
    "/posts",
    response_model=BlogPostRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[ADMIN],
)
async def create_blog_post(
    post: BlogPostCreate,
    background: BackgroundTasks,
    db: AsyncSession = Depends(get_async_session),
):
    """Crear un nuevo post en el blog"""
    try:
        nuevo_post = await svc.crear_post(db, post.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # Si el post está marcado como publicado → notificar
    if nuevo_post.publicado:
        emails = await list_emails(db)
        for e in emails:
            background.add_task(send_html, e, nuevo_post.titulo, nuevo_post.contenido)

    return nuevo_post


@router.get("/posts", response_model=List[BlogPostRead])
async def read_all_blog_posts(
    offset: int = 0,
    limit: int = 100,
    tag: Optional[str] = None,
    solo_publicados: bool = False,
    db: AsyncSession = Depends(get_async_session),
):
    """Obtener lista paginada de posts de blog"""
    return await svc.listar_posts(db, offset, limit, tag, solo_publicados)


@router.get("/posts/{post_id}", response_model=BlogPostRead)
async def read_blog_post(post_id: int, db: AsyncSession = Depends(get_async_session)):
    """Obtener un post de blog por su ID"""
    post = await svc.obtener_post(db, post_id)

    if not post:
        not_found("Post de blog")

    return post


@router.put("/posts/{post_id}", response_model=BlogPostRead)
async def update_blog_post(
    post_id: int,
    post_update: BlogPostUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """Actualizar un post de blog"""
    try:
        post = await svc.actualizar_post(
            db,
            post_id,
            post_update.model_dump(exclude_unset=False, exclude_none=True),
        )

        if not post:
            not_found("Post de blog")

        return post
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/posts/{post_id}", response_model=BlogPostRead)
async def partial_update_blog_post(
    post_id: int,
    post_update: BlogPostUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """Actualizar parcialmente un post de blog"""
    try:
        post = await svc.actualizar_post(
            db,
            post_id,
            post_update.model_dump(exclude_unset=True, exclude_none=True),
        )

        if not post:
            not_found("Post de blog")

        return post
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog_post(post_id: int, db: AsyncSession = Depends(get_async_session)):
    """Eliminar un post de blog"""
    post = await svc.borrar_post(db, post_id)

    if not post:
        not_found("Post de blog")

    # No content returned
    return None


@router.get("/posts/search/{term}", response_model=List[BlogPostRead])
async def search_blog_posts(
    term: str,
    offset: int = 0,
    limit: int = 100,
    solo_publicados: bool = False,
    db: AsyncSession = Depends(get_async_session),
):
    """Buscar posts de blog por término"""
    return await svc.buscar_posts(db, term, offset, limit, solo_publicados)


@router.get("/posts/categoria/{categoria}", response_model=List[BlogPostRead])
async def buscar_blogposts_por_categoria(
    categoria: str, db: AsyncSession = Depends(get_async_session)
):
    """Buscar posts de blog por categoría (tag)"""
    # Use a raw SQL text filter for LIKE
    result = await db.execute(
        select(BlogPost).where(text(f"tags LIKE '%{categoria}%'"))
    )
    return result.scalars().all()


@router.get("/posts/autor/{autor}", response_model=List[BlogPostRead])
async def buscar_blogposts_por_autor(
    autor: str, db: AsyncSession = Depends(get_async_session)
):
    """Buscar posts de blog por autor"""
    result = await db.execute(select(BlogPost).where(BlogPost.autor == autor))
    return result.scalars().all()
