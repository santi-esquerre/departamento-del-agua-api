from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import get_async_session
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import authenticate_admin
import asyncio

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_async_session)):
    token = await authenticate_admin(db, data.username, data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas"
        )
    return {"access_token": token, "token_type": "bearer"}
