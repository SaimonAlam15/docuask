from pydantic import Field
from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT")

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}"