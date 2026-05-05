import sys
from pathlib import Path
from typing import Any

from fastapi.responses import HTMLResponse
from pydantic_settings import BaseSettings

APP_DIR = Path(__file__).resolve().parent
BIN_DIR = Path(sys.executable).parent


class Settings(BaseSettings):
    APP_DIR: Path = APP_DIR
    BIN_DIR: Path = BIN_DIR

    STATIC_DIR: Path = APP_DIR / "static"
    TEMPLATE_DIR: Path = APP_DIR / "templates"

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/app"

    FASTAPI_PROPERTIES: dict[str, Any] = {
        "title": "Luigi's Pizza",
        "default_response_class": HTMLResponse,
    }

    DISABLE_DOCS: bool = True

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        fastapi_kwargs = self.FASTAPI_PROPERTIES

        if self.DISABLE_DOCS:
            fastapi_kwargs.update(
                {
                    "openapi_url": None,
                    "openapi_prefix": None,
                    "docs_url": None,
                    "redoc_url": None,
                }
            )
        return fastapi_kwargs


settings = Settings()
