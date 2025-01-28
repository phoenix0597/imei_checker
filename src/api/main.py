from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.api.controllers import (
    # auth,
    imei,
)
from src.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up IMEI Checker API")
    yield
    logger.info("Shutting down IMEI Checker API")


app = FastAPI(
    title="IMEI Checker API",
    description="API for checking IMEI numbers",
    version="1.0.0",
    lifespan=None,
)

# настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(auth.router)
app.include_router(imei.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
