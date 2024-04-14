import uvicorn
from fastapi import FastAPI

from contextlib import asynccontextmanager
from asyncio import create_task
from sys import exit

from api.main import api_router
from api.handler import AppHandler

API_ROUTE = "/api/v0"


@asynccontextmanager
async def lifespan(_: FastAPI):
    app_handler = AppHandler()
    create_task(app_handler.start())
    yield


app = FastAPI(title="Infomate", lifespan=lifespan)

app.include_router(api_router, prefix=API_ROUTE)


if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        exit(1)
