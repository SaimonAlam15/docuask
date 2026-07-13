from pydantic import Field
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    project_name: str = Field(alias="PROJECT_NAME")
    api_port: int = Field(alias="API_PORT")