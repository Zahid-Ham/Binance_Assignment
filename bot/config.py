"""Configuration loader and validator for the Trading Bot.

Loads variables from environment or .env files using Pydantic Settings
and validates required parameters.
"""

from typing import Optional
from dotenv import load_dotenv
from pydantic import SecretStr, field_validator, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from bot.exceptions import ConfigurationException

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings schema and loader.

    Validates presence of API credentials and URL formatting.
    """
    BINANCE_API_KEY: SecretStr
    BINANCE_SECRET_KEY: SecretStr
    BASE_URL: str = "https://testnet.binancefuture.com"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("BINANCE_API_KEY", "BINANCE_SECRET_KEY")
    @classmethod
    def validate_non_empty(cls, v: SecretStr) -> SecretStr:
        """Verify the secrets are not empty strings."""
        if not v.get_secret_value().strip():
            raise ValueError("Value cannot be blank or empty.")
        return v

    @field_validator("BASE_URL")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Ensure the BASE_URL has a correct HTTP/HTTPS scheme."""
        v_stripped = v.strip()
        if not (v_stripped.startswith("https://") or v_stripped.startswith("http://")):
            raise ValueError("URL must start with http:// or https://")
        return v_stripped


def load_config() -> Settings:
    """Load settings and raise ConfigurationException on validation errors.

    Returns:
        Settings: Validated configuration settings.

    Raises:
        ConfigurationException: If credentials are missing or invalid.
    """
    try:
        return Settings()
    except ValidationError as e:
        missing_fields = []
        for error in e.errors():
            loc = " -> ".join(str(x) for x in error.get("loc", []))
            msg = error.get("msg", "Validation failed")
            missing_fields.append(f"{loc}: {msg}")
        errors_str = "; ".join(missing_fields)
        raise ConfigurationException(
            f"Configuration load failed: {errors_str}"
        ) from e
    except Exception as e:
        raise ConfigurationException(f"Unexpected configuration error: {e}") from e
