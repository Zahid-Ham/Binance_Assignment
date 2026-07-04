import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator, SecretStr
from bot.exceptions import ConfigurationError

# Load environment variables from .env file
load_dotenv()


class Settings(BaseModel):
    """
    Application settings and validation using Pydantic.
    Loads values from environment variables.
    """
    BINANCE_API_KEY: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("BINANCE_API_KEY", ""))
    )
    BINANCE_SECRET_KEY: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("BINANCE_SECRET_KEY", ""))
    )
    BASE_URL: str = Field(
        default_factory=lambda: os.getenv("BASE_URL", "https://testnet.binancefuture.com")
    )
    LOG_LEVEL: str = Field(
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO")
    )

    @field_validator("BINANCE_API_KEY", "BINANCE_SECRET_KEY")
    @classmethod
    def validate_keys(cls, v: SecretStr) -> SecretStr:
        if not v.get_secret_value():
            raise ValueError("API Key and Secret Key must be set.")
        return v

    @field_validator("BASE_URL")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v.startswith("https://") and not v.startswith("http://"):
            raise ValueError("BASE_URL must be a valid URL starting with http:// or https://")
        return v


def load_config() -> Settings:
    """
    Load settings and raise ConfigurationError if validation fails.
    """
    try:
        return Settings()
    except Exception as e:
        raise ConfigurationError(f"Failed to load configuration: {e}") from e
