import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Azure Gateway Microservice",
    description="API Gateway for AZ-204",
    version="1.0.0",
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

# Configure CORS for development
origins = [
    "http://localhost:5173",  # Vite dev server
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specify which origins are allowed
    allow_credentials=True,  # Allow cookies to be included in requests
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
    expose_headers=[
        "Content-Disposition",
        "Cache-Control",
        "Content-Type",
    ],  # Important for SSE and downloads
)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
    )
