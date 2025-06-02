from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import async_session_factory


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


from fastapi import Header, HTTPException, status, Depends
from jose import JWTError
from sqlalchemy.future import select
from app.security import decode_token
from app.models import Admin


async def get_current_admin(
    authorization: str = Header(...), db: AsyncSession = Depends(get_async_session)
) -> Admin:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token faltante"
        )
    token = authorization.removeprefix("Bearer ").strip()
    try:
        payload = decode_token(token)
        admin_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido"
        )
    result = await db.execute(select(Admin).where(Admin.id == admin_id))
    admin = result.scalar_one_or_none()
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return admin
