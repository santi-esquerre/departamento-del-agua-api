from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.subscriber import Subscriber
from fastapi import HTTPException, status


async def add_subscriber(db: AsyncSession, email: str) -> Subscriber:
    exists = await db.execute(select(Subscriber).where(Subscriber.email == email))
    if exists.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email duplicado"
        )
    sub = Subscriber(email=email)
    db.add(sub)
    await db.commit()
    await db.refresh(sub)
    return sub


async def list_emails(db: AsyncSession) -> list[str]:
    result = await db.execute(select(Subscriber.email))
    return [row[0] for row in result.all()]
