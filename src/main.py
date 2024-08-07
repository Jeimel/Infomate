from os import chdir, path
from pathlib import Path

chdir(Path(__file__).parent.resolve())

from uvicorn import run
from fastapi import FastAPI
from sys import exit
from dotenv import load_dotenv

from api.main import api_router
from api.routes.apps import lifespan, ENV_PATH


API_ROUTE = "/api"


app = FastAPI(title="Infomate", lifespan=lifespan)
app.include_router(api_router, prefix=API_ROUTE)


if __name__ == "__main__":
    if not path.exists(ENV_PATH):
        with open(ENV_PATH, "w"):
            pass

    if not load_dotenv(ENV_PATH):
        exit(0)

    try:
        run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        exit(0)
