import datetime
from typing import TYPE_CHECKING
from uuid import uuid4
from sqlmodel import Field, Relationship, SQLModel

from core.models.message_model import Message

if TYPE_CHECKING:
    from core.models.article_model import Article


class Chat(SQLModel, table=True):

    __tablename__ = "AIN_CHATS"

    id: str = Field(primary_key=True, default_factory=lambda: str(uuid4()))
    name: str
    article_id: str | None = Field(foreign_key="AIN_ARTICLES.id")
    article: "Article" = Relationship(back_populates="chats")
    messages: list["Message"] = Relationship(back_populates="chat")
    created_at: datetime.datetime = Field(default_factory=lambda: str(datetime.datetime.now()))

    class Config:
        from_attributes = True