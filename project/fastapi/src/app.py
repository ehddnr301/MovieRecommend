"""Application module."""

from fastapi import FastAPI

from src.containers import Container
from src.core import Config
from src.api import router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


app = create_app()


@app.on_event("startup")
async def startup():
    container = Container()

    db = container.db()
    app.container = container

    if Config.ENV != "development":
        return

    await db.create_database()
