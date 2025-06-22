import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.db.database import init_database
from app.api.routes import router
from app.services.rabbitmq_service import rabbitmq_consumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle management
    Initialize database and RabbitMQ consumer on startup
    """
    # Startup
    try:
        await init_database()
        logger.info("Database initialized")
        
        await rabbitmq_consumer.connect()
        logger.info("RabbitMQ consumer started")
        
        logger.info("Image service startup completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to start image service: {e}")
        raise

    yield

    # Shutdown
    try:
        await rabbitmq_consumer.close()
        logger.info("Application shutdown completed")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


app = FastAPI(
    title="Azure Image Microservice",
    description="Image processing service for AZ-204",
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
