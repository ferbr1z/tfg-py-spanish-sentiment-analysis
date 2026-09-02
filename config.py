import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Falta configurar {name} en .env")
    return value


DB_NAME = required_env("DB_NAME")
DB_USER = required_env("DB_USER")
DB_PASSWORD = required_env("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_DRIVER = os.getenv("DB_DRIVER", "postgresql+psycopg")
DB_ECHO = os.getenv("DB_ECHO", "false").lower() == "true"

SHEET_ID = required_env("SHEET_ID")
COUNTRY = required_env("COUNTRY")

PAGE_DEPTH = int(required_env("PAGE_DEPTH"))
PAGES_PER_STEP = int(os.getenv("PAGES_PER_STEP", "2"))

# Lotes seguidos sin posts nuevos para dar por agotado un subtema.
# Subirlo da margen ante fallos puntuales de X.
EMPTY_STREAK_LIMIT = int(os.getenv("EMPTY_STREAK_LIMIT", "3"))

USE_OLD = os.getenv("USE_OLD", "false").lower() == "true"

AUTH_TOKEN = os.getenv("AUTH_TOKEN")
CT0 = os.getenv("CT0")
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

if USE_OLD:
    AUTH_TOKEN = required_env("AUTH_TOKEN")
    CT0 = required_env("CT0")
else:
    X_BEARER_TOKEN = required_env("X_BEARER_TOKEN")
