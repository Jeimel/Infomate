from fastapi import APIRouter

from api.routes import account, apps

api_router = APIRouter()
api_router.include_router(account.router, prefix="/account", tags=["account"])
api_router.include_router(apps.router, prefix="/apps", tags=["apps"])
