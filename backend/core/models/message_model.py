import json
from typing import TYPE_CHECKING
from uuid import uuid4
from datetime import datetime

from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from core.models.chat_model import Chat

class Message(SQLModel, table=True):
    __tablename__ = "AIN_MESSAGES"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    content: str
    role: str
    chat_id: str | None = Field(foreign_key="AIN_CHATS.id")
    is_visible: bool = Field(default=True)
    chat: "Chat" = Relationship(back_populates="messages")
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True