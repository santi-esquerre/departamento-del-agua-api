import os

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport  # Import ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlmodel import SQLModel

from app.db import get_session  # Corrected import for get_session
from app.main import app

ASYNC_URL = "sqlite+aiosqlite:///:memory:"  # In-memory SQLite for tests
engine_test = create_async_engine(ASYNC_URL, echo=False, future=True)

# Use async_sessionmaker for SQLAlchemy 1.4+ style
async_session_factory = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def anyio_backend():  # evita warning asyncio_mode
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def _create_schema():
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@pytest.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:  # Correct type hint
    async with async_session_factory() as session:
        yield session


@pytest.fixture
async def client(
    db: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:  # Correct type hint and db type
    # Correctly override dependencies. Assuming get_session is the primary one.
    app.dependency_overrides[get_session] = lambda: db

    # Use ASGITransport for testing FastAPI apps with httpx
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c

    # Clean up overrides after test
    app.dependency_overrides.clear()


@pytest.fixture(scope="session", autouse=True)
def _init_app_db():
    # Ensure app.db tables are created for the app's engine
    import app.db

    asyncio.get_event_loop().run_until_complete(app.db.init_db())
