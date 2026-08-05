from pydantic import BaseModel, ConfigDict, SecretStr


class AppConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    port: int


class DatabaseConfig(BaseModel):
    host: str
    port: int
    user: str
    password: SecretStr
    name: str

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.user}:"
            f"{self.password.get_secret_value()}@"
            f"{self.host}:"
            f"{self.port}/"
            f"{self.name}"
        )


class RedisConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    host: str
    port: int


class StorageConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    upload_directory: SecretStr
    provider: str


class OpenAIConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    api_key: SecretStr
