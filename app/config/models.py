from pydantic import BaseModel, ConfigDict, SecretStr

class AppConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    port: int


class DatabaseConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    host: str
    port: int
    user: str
    password: SecretStr
    name: str


class RedisConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    host: str
    port: int


class StorageConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    upload_directory: SecretStr


class OpenAIConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    api_key: SecretStr