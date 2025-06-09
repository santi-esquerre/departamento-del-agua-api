from os import getenv
from typing import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")

is_async = "+asyncpg" in DATABASE_URL or "+aiosqlite" in DATABASE_URL

# Only add connect_args for Postgres
if DATABASE_URL.startswith("postgresql"):
    connect_args = {"server_settings": {"timezone": "UTC"}}
else:
    connect_args = {}

if is_async:
    from sqlalchemy.ext.asyncio import (
        AsyncEngine,
        AsyncSession,
        create_async_engine,
        async_sessionmaker,
    )

    async_engine: AsyncEngine = create_async_engine(
        DATABASE_URL,
        echo=True,
        future=True,
        connect_args=connect_args,
    )
    async_session_factory = async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async def get_session_async() -> AsyncGenerator[AsyncSession, None]:
        async with async_session_factory() as session:
            yield session

    async def init_db_async() -> None:
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    get_session = get_session_async
    init_db = init_db_async
else:
    # Always define async_session_factory for test/fixture compatibility
    from sqlalchemy.ext.asyncio import (
        async_sessionmaker,
        AsyncSession,
        create_async_engine,
    )

    dummy_async_engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:", echo=False, future=True
    )
    async_session_factory = async_sessionmaker(
        dummy_async_engine, class_=AsyncSession, expire_on_commit=False
    )

    def get_session_sync():
        raise NotImplementedError("Async session not available for sync driver.")

    async def init_db_sync():
        raise NotImplementedError("Async init_db not available for sync driver.")

    get_session = get_session_sync
    init_db = init_db_sync

# Synchronous engine/session for scripts and sync routes
from sqlmodel import SQLModel, Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_sync_session_local():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlmodel import Session

    engine = create_engine(db_url, echo=True, future=True)
    return sessionmaker(class_=Session, autocommit=False, autoflush=False, bind=engine)


# For backward compatibility, keep the old SessionLocal (but warn)
try:
    SessionLocal = get_sync_session_local()
except Exception:
    SessionLocal = None
