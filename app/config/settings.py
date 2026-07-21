from pydantic_settings import BaseSettings, SettingsConfigDict


from app.config.models import (
    AppConfig,
    DatabaseConfig,
    OpenAIConfig,
    RedisConfig,
    StorageConfig
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='__',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    app: AppConfig
    database: DatabaseConfig
    redis: RedisConfig
    storage: StorageConfig
    openai: OpenAIConfig
