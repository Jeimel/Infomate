import sys

from fastapi import APIRouter

from api.handler import AppHandler
from api.routes import account, apps

try:
    api_router = APIRouter()
    api_router.include_router(account.router, prefix="/account", tags=["account"])
    api_router.include_router(apps.router, prefix="/apps", tags=["apps"])

    app_handler = AppHandler()
except KeyboardInterrupt:
    sys.exit(0)
