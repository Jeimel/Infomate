import uvicorn
from fastapi import FastAPI

from api.main import api_router
from api.handler import AppHandler

API_ROUTE = "/api/v0"

app = FastAPI(
    title="Infomate",
)

app.include_router(api_router, prefix=API_ROUTE)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    app_handler = AppHandler()
    app_handler.start()
