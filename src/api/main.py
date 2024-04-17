from fastapi import APIRouter

from api.routes import apps, device


api_router = APIRouter()
api_router.include_router(device.router, prefix="/device", tags=["device"])
api_router.include_router(apps.router, prefix="/apps", tags=["apps"])
