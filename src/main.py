from os import chdir
from pathlib import Path

chdir(Path(__file__).parent.resolve())

from uvicorn import run
from fastapi import FastAPI
from sys import exit

from api.main import api_router
from api.routes.apps import lifespan, app_handler


API_ROUTE = "/api"


app = FastAPI(title="Infomate", lifespan=lifespan)

app.include_router(api_router, prefix=API_ROUTE)


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
