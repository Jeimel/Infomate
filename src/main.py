from fastapi import FastAPI

from api.main import api_router

API_ROUTE = "/api/v0"

app = FastAPI(
    title="Infomate",
)

app.include_router(api_router, prefix=API_ROUTE)
