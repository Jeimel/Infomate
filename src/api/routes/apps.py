from fastapi import FastAPI, APIRouter, HTTPException
from yaml import safe_load
from os import walk, getcwd, getenv, environ
from dotenv import set_key, load_dotenv
from importlib import import_module
from contextlib import asynccontextmanager
from asyncio import create_task

from api.handler import AppHandler


APPS_DIRECTORY = getcwd() + "/apps"
ENV_PATH = getcwd() + "/.env"


def load_config(path: str) -> dict:
    with open(path + "/manifest.yaml", "r") as file:
        return safe_load(file)


def load_apps():
    apps_iter = walk(APPS_DIRECTORY)

    manifests = []
    paths = {}
    for root, _, files in apps_iter:
        if len(files) != 2 or "manifest.yaml" not in files:
            continue

        manifest = load_config(root)
        manifests.append(manifest)
        paths.update(
            {
                manifest["id"]: (
                    "apps." + manifest["id"] + "." + manifest["id"],
                    manifest["name"],
                )
            }
        )

    return manifests, paths


APP_MANIFESTS, APP_PATHS = load_apps()


router = APIRouter()
app_handler = AppHandler()


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_task(app_handler.start())
    yield
    app_handler.running = False


@router.get("/")
def apps() -> dict:
    return {"Apps": APP_MANIFESTS}


@router.post("/{app_id}/deploy")
def deploy(app_id: str) -> bool:
    if app_id not in APP_PATHS:
        raise HTTPException(status_code=404, detail="App not found.")

    try:
        path, app_name = APP_PATHS[app_id]
        module = import_module(path)
        app_handler.set_next(getattr(module, app_name))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Can't load app.")

    return True

@router.post("/{app_id}/variables")
def data(app_id: str, name: str, value: str) -> bool:
    if app_id not in APP_PATHS:
        raise HTTPException(status_code=404, detail="App not found.")

    try:
        path, app_name = APP_PATHS[app_id]
        module = import_module(path)
        app = getattr(module, app_name)

        env = app.env()
        variables = app.variables()
    except:
        raise HTTPException(status_code=500, detail="Can't load app.")

    if not env:
        raise HTTPException(status_code=404, detail="App doesn't support variables.")

    if name not in variables:
        raise HTTPException(
            status_code=404, detail="Provided variable isn't supported."
        )

    set_key(dotenv_path=ENV_PATH, key_to_set="{}_{}".format(app_name.upper(), name), value_to_set=value)
    return load_dotenv(ENV_PATH)
