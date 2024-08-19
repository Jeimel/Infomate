from fastapi import APIRouter
from logging import getLogger, DEBUG, StreamHandler, Formatter
from io import StringIO

from api.routes import apps, device


api_router = APIRouter()
api_router.include_router(device.router, prefix="/device", tags=["device"])
api_router.include_router(apps.router, prefix="/apps", tags=["apps"])

logger = getLogger("uvicorn")
logger.setLevel(DEBUG)

logger_buffer = StringIO()
handler = StreamHandler(logger_buffer)
handler.setLevel(DEBUG)

formatter = Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)
