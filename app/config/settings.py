from functools import lru_cache

from app.config.app import AppSettings
from app.config.database import DatabaseSettings
from app.config.openai import OpenAISettings
from app.config.redis import RedisSettings
from app.config.storage import StorageSettings


class Settings:
    def __init__(self):
        self.app = AppSettings()
        self.database = DatabaseSettings()
        self.redis = RedisSettings()
        self.storage = StorageSettings()
        self.openai = OpenAISettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()