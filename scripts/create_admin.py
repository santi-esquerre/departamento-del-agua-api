# scripts/create_admin.py
import os
import sys
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import get_sync_session_local
from app.services.auth_service import create_admin


def get_sync_db_url():
    url = os.environ.get("DATABASE_URL")
    if url and url.startswith("postgresql+asyncpg://"):
        # switch back to the sync driver
        return url.replace("postgresql+asyncpg://", "postgresql://", 1)
    return url


async def main():
    # If you’re pointing at an async URL, switch it to sync
    sync_url = get_sync_db_url()
    if sync_url:
        os.environ["DATABASE_URL"] = sync_url

    # Obtain a sync Session (can be used by create_admin)
    SessionLocal = get_sync_session_local()
    with SessionLocal() as session:
        # *** Await the coroutine! ***
        await create_admin(session, "admin", "admin123")
        print("✅ Admin user created")


if __name__ == "__main__":
    asyncio.run(main())
