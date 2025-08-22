"""Application configuration settings."""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = "Menu Minglers"
    app_version: str = "0.1.0"
    debug: bool = Field(default=False, env="DEBUG")
    app_env: str = Field(default="development", env="APP_ENV")

    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")

    # API
    api_v1_prefix: str = "/api/v1"
    docs_url: Optional[str] = "/docs"
    redoc_url: Optional[str] = "/redoc"

    # Azure OpenAI
    azure_openai_key: str = Field(default="", env="AZURE_OPENAI_KEY")
    azure_openai_endpoint: str = Field(default="", env="AZURE_OPENAI_ENDPOINT")

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


# Global settings instance
settings = Settings()
