from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import get_async_session
from app.schemas.subscriber import SubscriberCreate, SubscriberRead
from app.services.subscriber_service import add_subscriber

router = APIRouter(prefix="/suscriptores", tags=["Suscriptores"])


@router.post("/", response_model=SubscriberRead, status_code=201)
async def subscribe(
    data: SubscriberCreate, db: AsyncSession = Depends(get_async_session)
):
    try:
        return await add_subscriber(db, data.email)
    except HTTPException as exc:
        raise exc
