import logging
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.db.database import init_database
from app.api.routes import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle management
    Initialize database on startup, cleanup on shutdown
    """
    await init_database()
    logger.info("Database initialized")
    yield
    logger.info("Application shutdown")


app = FastAPI(
    title="Azure Auth Microservice",
    description="Authentication service for AZ-204",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
    )
