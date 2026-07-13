from pydantic import Field
from pydantic_settings import BaseSettings


class StorageSettings(BaseSettings):
    upload_directory: str = Field(alias="UPLOAD_DIRECTORY")