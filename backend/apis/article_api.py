import re
import httpx
from bs4 import BeautifulSoup
import openai
from sqlmodel import Session
from apis.chat_api import add_message, init_chat
from core.config.db_init import get_session_db
from core.models.article_model import Article
from core.schemas.article_schemas import ArticleSendSerializer

async def fetch_article_content(article_url: ArticleSendSerializer) -> str:
    """
    Fetches the content of an article from the given URL.

    Args:
        article_url (ArticleSendSerializer): The URL of the article.

    Returns:
        str: The content of the article.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(str(article_url.url))
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.getText(separator='\n', strip=False)
        return text

def get_title(*, article_content: str) -> str:
    """
    Extracts the title of an article from its content.

    Args:
        article_content (str): The content of the article.

    Returns:
        str: The title of the article.
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Generate a title for the article with a maximum of 5 words and just give me text without any quotation marks or anything else:"},
            {"role": "user", "content": article_content},
        ]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

async def get_summary(*, article_url: ArticleSendSerializer, session: Session = get_session_db()):
    """
    Generates a summary of an article.

    Args:
        article_url (ArticleSendSerializer): The URL of the article.
        session (Session, optional): The database session. Defaults to get_session_db().

    Returns:
        dict: A dictionary containing the summary message, chat ID, and the summary content.
    """
    response = await fetch_article_content(article_url)
    clean_text = re.sub(r'\s+', ' ', response).strip()
    article = Article(url=article_url.url)
    title = get_title(article_content=clean_text)
    chat = init_chat(article_url=article, chat_title=title, session=session)
    add_message(content=clean_text, role="user", chat_id=chat.id, session=session, is_visible=False)

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "The following is a summary of the article:"},
            {"role": "user", "content": clean_text},
        ]
    )

    message = add_message(content=response.choices[0].message.content, role="assistant", chat_id=chat.id, session=session)
    return {"message": message, "chat_id": chat.id, "title": title}
