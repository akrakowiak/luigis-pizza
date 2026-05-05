from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.db import add_example_data, create_db_and_tables
from app.routes import router
from app.tailwind import run_tailwind


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    add_example_data()
    yield


def get_app() -> FastAPI:
    app = FastAPI(**settings.fastapi_kwargs, lifespan=lifespan)
    app.include_router(router)
    app.mount("/static", StaticFiles(directory="app/static"), name="app/static")

    return app


app = get_app()


def dev():
    main(True)


def main(dev: bool = False):
    import uvicorn

    run_tailwind(dev)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=dev)


if __name__ == "__main__":
    main()
