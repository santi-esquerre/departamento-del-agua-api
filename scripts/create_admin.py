import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session
from app.db import SessionLocal, get_sync_session_local
from app.services.auth_service import create_admin


def get_sync_db_url():
    url = os.environ.get("DATABASE_URL")
    if url and url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql+asyncpg://", "postgresql://", 1)
    return url


if __name__ == "__main__":
    # Patch DATABASE_URL to sync driver if needed
    sync_url = get_sync_db_url()
    if sync_url:
        os.environ["DATABASE_URL"] = sync_url
    SessionLocal = get_sync_session_local()
    with SessionLocal() as s:
        create_admin(s, "admin", "admin123")  # type: ignore
