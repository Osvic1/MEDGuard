import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # Points to MEDGuard/


class Config:
    # App
    APP_NAME: str = "MedGuard"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    # No fallback; enforce environment variable
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "5000"))

    # Database
    DB_PATH: Path = Path(os.getenv("DB_PATH", BASE_DIR / "medguard.db"))

    # Security (QR signing, etc.)
    QR_SIGNING_SECRET: str = os.getenv(
        "QR_SIGNING_SECRET", "sign-me-in-prod")  # Update in prod

    # CORS
    CORS_ORIGINS: list = os.getenv(
        "CORS_ORIGINS", "*").split(",")  # List for flask-cors

    # Paths for frontend
    TEMPLATES_DIR: Path = BASE_DIR / "frontend" / "templates"
    STATIC_DIR: Path = BASE_DIR / "frontend" / "static"

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


class ProdConfig(Config):
    DEBUG = False
    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS", "https://your-domain.com").split(",")  # List
    # Enforce environment variable in prod
    SECRET_KEY = os.getenv("SECRET_KEY")


def get_config():
    """
    Return the configuration object based on the environment.
    """
    env = os.getenv("ENV", "dev").lower()
    if env in ("prod", "production"):
        return ProdConfig()
    return Config()
