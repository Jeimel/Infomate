from fastapi import APIRouter

from api.handler import AppHandler
from api.routes import account, apps
from apps.clock.clock import Clock

api_router = APIRouter()

api_router.include_router(account.router, prefix="/account", tags=["account"])
api_router.include_router(apps.router, prefix="/apps", tags=["apps"])


clock = Clock()
app_handler = AppHandler(clock)
