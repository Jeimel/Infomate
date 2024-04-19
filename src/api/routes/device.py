from fastapi import APIRouter, HTTPException, Path
from socket import gethostname
from subprocess import Popen, PIPE
from typing import Annotated

from config import LED_BRIGHTNESS
from api.routes.apps import app_handler


router = APIRouter()


@router.get("/")
def device():
    return {"name": gethostname(), "brightness": LED_BRIGHTNESS}


@router.post("/update")
def update():
    process = Popen(["git", "pull"], stdout=PIPE)

    try:
        output = process.communicate(timeout=10)[1]
        process.kill()

        return output != b""
    except:
        raise HTTPException(status_code=500, detail="Can't update repository.")


@router.post("/brightness")
def brightness(
    brightness: Annotated[int, Path(title="The ID of the item to get", ge=1, le=100)]
):
    app_handler.matrix.brightness = brightness
    return True
