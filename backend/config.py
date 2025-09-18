import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # points to medguard/


class Config:
    # App
    APP_NAME: str = "MedGuard"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-in-prod")
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "5000"))

    # Database
    DB_PATH: Path = Path(os.getenv("DB_PATH", BASE_DIR / "medguard.db"))

    # Security (QR signing, etc.)
    QR_SIGNING_SECRET: str = os.getenv("QR_SIGNING_SECRET", "sign-me-in-prod")

    # CORS
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")  # tighten in prod

    # Paths for frontend
    TEMPLATES_DIR: Path = BASE_DIR / "frontend" / "templates"
    STATIC_DIR: Path = BASE_DIR / "frontend" / "static"

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


class ProdConfig(Config):
    DEBUG = False
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "https://your-domain.com")


def get_config():
    env = os.getenv("ENV", "dev").lower()
    if env in ("prod", "production"):
        return ProdConfig()
    return Config()
