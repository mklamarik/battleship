import logging
from uuid import UUID

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "Battleships API"
    debug: bool = False
    default_uuid: UUID = UUID("{00000000-0000-0000-0000-000000000000}")
    rng_seed: int | None = None
    log_level: int = logging.DEBUG

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
