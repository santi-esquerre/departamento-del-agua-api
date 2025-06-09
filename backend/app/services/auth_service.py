from sqlmodel import Session, select
from app.models import Admin
from app.security import verify_password, hash_password, create_access_token
import asyncio


async def create_admin(db, username: str, password: str):
    admin = Admin(username=username, password_hash=hash_password(password))
    db.add(admin)
    if hasattr(db, "commit") and asyncio.iscoroutinefunction(db.commit):
        await db.commit()
        await db.refresh(admin)
    else:
        db.commit()
        db.refresh(admin)
    return admin


async def authenticate_admin(db, username: str, password: str) -> str | None:
    stmt = select(Admin).where(Admin.username == username)
    # AsyncSession: use execute + scalars().first()
    if hasattr(db, "execute") and asyncio.iscoroutinefunction(db.execute):
        result = await db.execute(stmt)
        admin = result.scalars().first()
    else:
        admin = db.exec(stmt).first()
    if admin and verify_password(password, admin.password_hash):
        return create_access_token({"sub": str(admin.id)})
    return None
