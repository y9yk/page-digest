import os
from functools import lru_cache
from os import path
from typing import List

from pydantic_settings import BaseSettings

from src.app.common.constant import APP_ENV


class Settings(BaseSettings):
    """
    기본 Configuration
    """

    PROJECT_ROOT: str = path.dirname(
        path.dirname(
            path.dirname(
                path.dirname(
                    (path.abspath(__file__)),
                ),
            ),
        )
    )

    PROJECT_NAME: str = "page-digest"
    PROJECT_DESC: str = ""

    DEBUG: bool = True

    # project
    API_PREFIX: str = f""

    DB_HOST: str = "localhost"
    DB_USER: str = "root"
    DB_PASS: str = "password"
    DB_NAME: str = "plus"
    DB_PORT: str = "3306"
    DB_POOL_PRE_PING: bool = True
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = False

    OPENAI_MODEL_NAME: str = "gpt-4o-mini"
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = ""
    OPENAI_TOKEN_LIMIT: int = 128000
    MAX_TOKENS: int = 4096 * 2
    EPSILON: int = 100

    # langfuse integration
    LANGFUSE_ENABLED: bool = False
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_HOST: str = ""

    class Config:
        env_prefix = ""
        env_file = f"{os.path.dirname(os.path.abspath(__file__))}/.env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


settings: Settings = get_settings()
