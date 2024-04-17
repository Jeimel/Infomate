from fastapi import APIRouter
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
    return process.communicate()[0]
