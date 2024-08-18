from fastapi import APIRouter, HTTPException, Path
from typing_extensions import Annotated
from socket import gethostname
from subprocess import Popen, PIPE
from logging import getLogger, DEBUG, StreamHandler, Formatter
from io import StringIO

from api.routes.apps import app_handler


router = APIRouter()

logger = getLogger("uvicorn")
logger.setLevel(DEBUG)

logger_buffer = StringIO()
handler = StreamHandler(logger_buffer)
handler.setLevel(DEBUG)

formatter = Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


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
    log_output = logger_buffer.getvalue().split("\n")
    return {"logs": log_output}


@router.post("/brightness")
def brightness(
    brightness: Annotated[
        int, Path(title="The brightness of the display", gt=0, le=100)
    ],
):
    app_handler.update_brightness(brightness)
    return True
