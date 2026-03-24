from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = 'URL Shortener'
    DEBUG: int = 0
    DATABASE_URL: str = 'postgresql://user:password@db:5432/url_shortener'
    SHORT_ID_LENGTH: int = Field(ge=1, le=32, default=6)  # max uuid.hex len is 32
    DOMEN: str = 'http://localhost:8000'

