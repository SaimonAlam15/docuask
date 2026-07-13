from pydantic import Field
from pydantic_settings import BaseSettings


class OpenAISettings(BaseSettings):
    api_key: str = Field(alias="OPENAI_API_KEY")