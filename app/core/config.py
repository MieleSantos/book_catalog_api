from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./books.db"
    APP_NAME: str = "Book Catalog API"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"


settings = Settings()
