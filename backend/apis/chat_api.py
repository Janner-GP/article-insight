from fastapi import HTTPException
import openai
from sqlmodel import Session, select

from core.config.db_init import get_session_db
from core.models.chat_model import Chat
from core.models.message_model import Message
from core.schemas.chat_schemas import MessageUser

# Lista para almacenar conexiones WebSocket activas
active_connections = []

def add_message(content: str, role: str, chat_id: str, session: Session, is_visible: bool = True) -> Message:
    """
    Add a new message to the chat.

    Args:
        content (str): The content of the message.
        role (str): The role of the sender (e.g., "user" or "assistant").
        chat_id (str): The ID of the chat.
        session (Session): The database session.

    Returns:
        Message: The newly created message.
    """
    message = Message(chat_id=chat_id, content=content, role=role, is_visible=is_visible)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message

def get_messages(*, chat_id: str, session: Session = get_session_db(), limit: int = 100000) -> list[Message]:
    """
    Retrieve messages from a chat.

    Args:
        chat_id (str): The ID of the chat.
        session (Session): The database session.
        limit (int, optional): The maximum number of messages to retrieve. Defaults to 100000.

    Returns:
        list[Message]: The list of retrieved messages.
    """
    try:
        messages = session.exec(select(Message).where(Message.chat_id == chat_id).limit(limit).order_by(Message.created_at)).all()
        if not messages:
            raise HTTPException(status_code=404, detail="Messages not found")
        return messages
    except:
        raise HTTPException(status_code=404, detail="Chat not found")

def init_chat(*, article_url: str, chat_title:str,  session: Session) -> Chat:
    """
    Initialize a new chat.

    Args:
        article_url (ArticleSendSerializer): The article URL associated with the chat.
        session (Session): The database session.

    Returns:
        Chat: The newly created chat.
    """
    chat = Chat(article_url=article_url, name=chat_title)
    session.add(chat)
    session.commit()
    return chat

async def conversation(*, chat_id: str, message: MessageUser, session: Session = get_session_db()):
    """
    Perform a conversation with the chatbot.

    Args:
        chat_id (str): The ID of the chat.
        message (MessageUser): The user's message.
        session (Session, optional): The database session. Defaults to get_session_db().

    Returns:
        dict: The response from the chatbot.
    """
    add_message(content=message.content, role="user", chat_id=chat_id, session=session)
    messages = get_messages(chat_id=chat_id, session=session, limit=30)
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": message.role, "content": message.content} for message in messages]
    )
    message = add_message(content=response.choices[0].message.content, role="assistant", chat_id=chat_id, session=session)
    return message

async def get_chats(*, session: Session = get_session_db()) -> list[Chat]:
    """
    Retrieves a list of Chat objects from the database.

    Parameters:
    - session: The database session to use. Defaults to the session returned by get_session_db().

    Returns:
    - A list of Chat objects retrieved from the database.
    """
    result = session.exec(select(Chat).order_by(Chat.created_at.desc())).all()
    return result

async def get_chat(*, chat_id: str, session: Session = get_session_db()) -> Chat:
    """
    Retrieve a chat by its ID.

    Args:
        chat_id (str): The ID of the chat to retrieve.
        session (Session, optional): The database session to use. Defaults to get_session_db().

    Returns:
        Chat: The retrieved chat object.

    """
    result = session.exec(select(Chat).where(Chat.id == chat_id)).first()
    return result