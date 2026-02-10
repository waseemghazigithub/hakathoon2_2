"""
Configuration module for loading and validating environment variables.

Implements FR-002 requirement for environment-based configuration.
"""
import os
import sys
from typing import Literal
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All settings are required unless explicitly marked optional.
    Application will fail fast on startup if required variables are missing.
    """

    # Database Configuration
    database_url: str = Field(
        ...,
        description="PostgreSQL connection string for Neon database"
    )

    # Authentication Configuration
    better_auth_secret: str = Field(
        ...,
        min_length=32,
        description="Shared secret for JWT verification (must match frontend)"
    )

    # CORS Configuration
    frontend_url: str = Field(
        default="http://localhost:3000",
        description="Frontend URL for CORS allowlist"
    )

    # Environment
    environment: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Deployment environment"
    )

    # OpenAI Configuration
    openai_api_key: str = Field(
        ...,
        description="OpenAI API Key for Agent"
    )
    openai_model: str = Field(
        default="gpt-4o-mini",
        description="OpenAI model to use"
    )
    openai_max_tokens: int = Field(
        default=4000,
        description="Max tokens for OpenAI response"
    )

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Ensure database URL is not empty and has correct format."""
        if not v:
            raise ValueError("DATABASE_URL environment variable is required")
        if not v.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError("DATABASE_URL must be a PostgreSQL connection string")
        return v

    @field_validator("better_auth_secret")
    @classmethod
    def validate_auth_secret(cls, v: str) -> str:
        """Ensure auth secret meets minimum security requirements."""
        if not v:
            raise ValueError("BETTER_AUTH_SECRET environment variable is required")
        if len(v) < 32:
            raise ValueError("BETTER_AUTH_SECRET must be at least 32 characters")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = False


def load_settings() -> Settings:
    """
    Load and validate settings from environment.

    Fails fast with clear error message if required variables are missing.
    """
    try:
        return Settings()
    except Exception as e:
        print(f"❌ Configuration Error: {e}", file=sys.stderr)
        print("\n💡 Please ensure your .env file exists and contains:", file=sys.stderr)
        print("   - DATABASE_URL (PostgreSQL connection string)", file=sys.stderr)
        print("   - BETTER_AUTH_SECRET (min 32 characters, must match frontend)", file=sys.stderr)
        print("   - FRONTEND_URL (optional, defaults to http://localhost:3000)", file=sys.stderr)
        print("   - ENVIRONMENT (optional, defaults to development)", file=sys.stderr)
        print("\nSee .env.example for template", file=sys.stderr)
        sys.exit(1)


# Global settings instance
settings = load_settings()