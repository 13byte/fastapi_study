from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    jwt_secret: str


@lru_cache
def get_settings() -> Settings:
    return Settings()
