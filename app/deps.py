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
