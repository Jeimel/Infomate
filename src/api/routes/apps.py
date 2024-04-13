from fastapi import APIRouter
import yaml

import os

APPS_DIRECTORY = os.getcwd() + "/apps"


def load_config(path: str):
    with open(path + "/manifest.yaml", "r") as file:
        return yaml.safe_load(file)


def load_apps():
    apps_iter = os.walk(APPS_DIRECTORY)

    apps = []
    for root, _, files in apps_iter:
        if not (root + ".py" in files and "manifest.yaml" in files):
            continue

        manifest = load_config(root)
        apps.append(manifest)

    return apps


APPS = load_apps()


router = APIRouter()


@router.get("/")
def available_apps():
    return {"Apps": APPS}


@router.delete("/{appID}")
def delete_app(appID: int):
    pass


@router.post("/{appID}/deploy")
def deploy_app(appID: int):
    pass
