from os import chdir
from pathlib import Path
chdir(Path(__file__).parent.resolve())

from uvicorn import run
from fastapi import FastAPI
from contextlib import asynccontextmanager
from sys import exit

from api.main import api_router
from api.handler import AppHandler
from api.routes.apps import lifespan


API_ROUTE = "/api"


# app_handler = AppHandler()

"""
@asynccontextmanager
async def lifespan(_: FastAPI):
    create_task(app_handler.start())
    yield
"""

app = FastAPI(title="Infomate", lifespan=lifespan)

app.include_router(api_router, prefix=API_ROUTE)


if __name__ == "__main__":
    try:
        run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        exit(1)
