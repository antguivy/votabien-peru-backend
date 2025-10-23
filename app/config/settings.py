from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=True
    )

    # === App Config (defaults OK) ===
    APP_NAME: str = "Backend"
    DEBUG: bool = False
    ENVIRONMENT: str = Field(
        default="development", pattern="^(development|staging|production)$"
    )

    # === Frontend (default OK para dev) ===
    FRONTEND_HOST: str = "http://localhost:3000"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    # === Database ===
    DATABASE_URI: str = Field(default="", description="Database connection string")

    # === security ===
    JWT_SECRET_KEY: str = Field(..., min_length=32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=15, ge=1, le=1440)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(default=10080, ge=1)
    REFRESH_TOKEN_SLIDING_WINDOW: bool = True
    REFRESH_TOKEN_RENEWAL_THRESHOLD_DAYS: int = 2

    # === Email (opcional) ===
    RESEND_API_KEY: str | None = None
    EMAIL_FROM: str | None = None

    # === CORS ===
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # === Validations ===
    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def validate_secrets_not_default(cls, v: str, info) -> str:
        """Evita usar secrets de ejemplo en producción"""
        if info.data.get("ENVIRONMENT") == "production":
            weak_secrets = [
                "dev-secret-not-for-production",
                "change-me",
                "secret",
            ]
            if v in weak_secrets or len(v) < 32:
                raise ValueError(
                    f"{info.field_name} must be strong in production (32+ chars)"
                )
        return v

    @field_validator("DATABASE_URI")
    @classmethod
    def validate_db_in_production(cls, v: str, info) -> str:
        """Base de datos obligatoria en producción"""
        env = info.data.get("ENVIRONMENT")
        if env == "production" and v.startswith("sqlite"):
            raise ValueError("SQLite not allowed in production")
        return v

    def model_post_init(self, __context) -> None:  # pylint: disable=arguments-differ
        """Post-inicialización automática"""
        if self.FRONTEND_HOST not in self.ALLOWED_ORIGINS:
            self.ALLOWED_ORIGINS.append(self.FRONTEND_HOST)

        if self.EMAIL_FROM is None:
            email_map = {
                "production": "noreply@votabienperu.com",
                "staging": "staging@votabienperu.com",
                "development": "dev@resend.dev",
            }
            self.EMAIL_FROM = email_map.get(self.ENVIRONMENT, "dev@resend.dev")  # pylint: disable=invalid-name


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore
