from pydantic import BaseModel


class MessageUser(BaseModel):
    content: str