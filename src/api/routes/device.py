from fastapi import APIRouter, HTTPException
from socket import gethostname
from subprocess import Popen, PIPE

from config import LED_BRIGHTNESS


router = APIRouter()


@router.get("/")
def device():
    return {"name": gethostname(), "brightness": LED_BRIGHTNESS}


@router.post("/update")
def update():
    process = Popen(["git", "pull"], stdout=PIPE)

    try:
        output = process.communicate(timeout=10)[0]
        process.kill()

        return output
    except:
        raise HTTPException(status_code=500, detail="Can't update repository.")
