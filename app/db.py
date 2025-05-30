from os import getenv
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker  # Corrected import
from sqlmodel import SQLModel

DATABASE_URL = getenv("DATABASE_URL")
if DATABASE_URL is None:  # Added check for DATABASE_URL
    raise ValueError("DATABASE_URL environment variable is not set")

# Only add connect_args for Postgres
if DATABASE_URL.startswith("postgresql"):
    connect_args = {"server_settings": {"timezone": "UTC"}}
else:
    connect_args = {}

async_engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    connect_args=connect_args,
)

# Use async_sessionmaker for AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

async_session_factory = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:  # Use the factory
        yield session


# al arrancar la app, sólo crea las tablas si es necesario:
async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
