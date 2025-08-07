from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = "URL Shortener"
    APP_VERSION: str = "1.0.0"
    BASE_URL: str = "http://localhost:8000"
    DATABASE_URL: str = "sqlite:///./shortener.db"

    class Config:
        env_file = ".env"


settings = Settings()
