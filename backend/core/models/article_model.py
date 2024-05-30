from uuid import uuid4
from datetime import datetime

from sqlmodel import Relationship, SQLModel, Field

from core.models.chat_model import Chat

class Article(SQLModel, table=True):

    __tablename__ = "AIN_ARTICLES"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    url: str
    chats: list["Chat"] =   Relationship(back_populates="article")
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
