from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, UniqueConstraint


class Subscriber(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("email"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, max_length=254)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
