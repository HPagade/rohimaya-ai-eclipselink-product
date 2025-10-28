"""
Configuration settings for EclipseLink AI Backend
Uses Pydantic Settings for type-safe environment variable management
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 4000

    # Security
    SECRET_KEY: str = "changeme-in-production-use-openssl-rand-hex-32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "*.rohimaya.ai"]

    # Database (Supabase PostgreSQL)
    DATABASE_URL: str = "postgresql://postgres:changeme@localhost:5432/eclipselink"

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""

    # OpenAI (Whisper for voice transcription)
    OPENAI_API_KEY: str = ""
    OPENAI_WHISPER_MODEL: str = "whisper-1"

    # Anthropic (Claude for SBAR generation)
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-sonnet-4-20250514"
    ANTHROPIC_MAX_TOKENS: int = 4096

    # Azure OpenAI (Optional - if user prefers Azure)
    AZURE_OPENAI_KEY: str = ""
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_DEPLOYMENT: str = ""
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"

    # File Upload (for voice recordings)
    MAX_UPLOAD_SIZE: int = 25 * 1024 * 1024  # 25MB (Whisper limit)
    ALLOWED_AUDIO_TYPES: List[str] = [
        "audio/wav",
        "audio/mpeg",
        "audio/mp3",
        "audio/mp4",
        "audio/m4a",
        "audio/webm"
    ]

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60

    # Email (for notifications)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "noreply@eclipselink.ai"

    # Rewards System
    POINTS_BASELINE_HANDOFF: int = 10
    POINTS_UPDATE_HANDOFF: int = 5
    POINTS_CRITICAL_ALERT: int = 15
    POINTS_PERFECT_SBAR: int = 5

    # Update-Only Model™ Settings
    BASELINE_MAX_AGE_HOURS: int = 24  # Force new baseline after 24 hours
    SIMILARITY_THRESHOLD: float = 0.85  # AI confidence threshold for change detection

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # HIPAA Compliance
    AUDIT_LOG_RETENTION_DAYS: int = 2555  # 7 years (HIPAA requirement)
    SESSION_TIMEOUT_MINUTES: int = 15
    PASSWORD_MIN_LENGTH: int = 12
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_DIGITS: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create global settings instance
settings = Settings()
