from pydantic import HttpUrl, BaseModel

class ArticleSendSerializer(BaseModel):
    url: HttpUrl