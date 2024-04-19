from fastapi import APIRouter, HTTPException, Path
from socket import gethostname
from subprocess import Popen, PIPE
from typing import Annotated

from api.routes.apps import app_handler


router = APIRouter()


@router.get("/")
def device():
    return {"name": gethostname(), "brightness": app_handler.matrix.brightness}


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
def brightness(brightness: int):
    if brightness < 1 or brightness > 100:
        raise HTTPException(
            status_code=422, detail="Brightness must be in range [1, 100]."
        )

    app_handler.matrix.brightness = brightness
    app_handler.app.canvas.brightness = brightness
    return True
