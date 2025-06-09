from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class SubscriberCreate(BaseModel):
    email: EmailStr


class SubscriberRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
