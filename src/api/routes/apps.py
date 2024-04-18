from fastapi import FastAPI, APIRouter, HTTPException
from yaml import safe_load
from os import walk, getcwd
from importlib import import_module
from contextlib import asynccontextmanager
from asyncio import create_task

from api.handler import AppHandler


APPS_DIRECTORY = getcwd() + "/apps"


def load_config(path: str) -> dict:
    with open(path + "/manifest.yaml", "r") as file:
        return safe_load(file)


def load_apps():
    apps_iter = walk(APPS_DIRECTORY)

    manifests = []
    paths = {}
    for root, _, files in apps_iter:
        if len(files) != 2 or "manifest.yaml" != files[0]:
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


@router.post("/{appID}/deploy")
def deploy(appID: str) -> bool:
    if appID not in APP_PATHS:
        raise HTTPException(status_code=404, detail="App not found.")

    try:
        path, name = APP_PATHS[appID]
        module = import_module(path)
        app_handler.set_next(getattr(module, name))
    except:
        raise HTTPException(status_code=500, detail="Can't load app.")

    return True
