import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router
from app.services.rabbitmq_service import rabbitmq_service
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle management
    Initialize RabbitMQ connection on startup
    """
    # Startup
    await rabbitmq_service.connect()
    logger.info("Gateway services initialized")
    
    yield
    
    # Shutdown
    await rabbitmq_service.close()
    logger.info("Gateway services shutdown")


app = FastAPI(
    title="Azure Gateway Microservice",
    description="API Gateway for AZ-204",
    version="1.0.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """
    Request logging middleware
    AZ-204 Pattern: Centralized logging and monitoring through gateway
    """

    start_time = datetime.now(timezone.utc)

    logger.info(f"Gateway: {request.method} {request.url.path}")

    response = await call_next(request)

    process_time = datetime.now(timezone.utc) - start_time

    logger.info(
        f"Gateway: {request.method} {request.url.path} - {response.status_code} - {process_time.total_seconds():.3f}s"
    )

    # Add custom headers for tracing (AZ-204: Distributed tracing patterns)
    response.headers["X-Process-Time"] = str(process_time.total_seconds())
    response.headers["X-Gateway-Version"] = "1.0.0"

    return response


app.include_router(router)

# Configure CORS origins from environment
origins = settings.cors_origins_list

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[
        "Content-Disposition",
        "Cache-Control",
        "Content-Type",
    ],
)

