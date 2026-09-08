from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DATABASE_PATH = Path(__file__).resolve().parents[2] / "data" / "database.db"


class Settings(BaseSettings):
    PROJECT_NAME: str = "Product listings API"
    VERSION: str = "0.1.0"

    DATABASE_URL: str = f"sqlite:///{DATABASE_PATH.as_posix()}"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
