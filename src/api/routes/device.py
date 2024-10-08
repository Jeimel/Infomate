from fastapi import APIRouter, HTTPException, Path
from typing_extensions import Annotated
from socket import gethostname
from subprocess import Popen, PIPE

from api.routes.apps import app_handler
from api.main import logger_buffer


router = APIRouter()


@router.get("/", tags=["device"])
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


@router.get("/logs")
def logs():
    output = logger_buffer.getvalue().split("\n")
    return {"logs": output}


@router.post("/brightness")
def brightness(
    brightness: Annotated[
        int, Path(title="The brightness of the display", gt=0, le=100)
    ],
):
    app_handler.update_brightness(brightness)
    return True
