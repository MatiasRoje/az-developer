import os
from typing import List


class Settings:
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8080"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")
    IMAGE_SERVICE_URL: str = os.getenv("IMAGE_SERVICE_URL", "http://image-service:8001")

    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

    MINIO_ENDPOINT: str = os.environ.get("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY: str = os.environ.get("MINIO_ACCESS_KEY", "azuredev")
    MINIO_SECRET_KEY: str = os.environ.get("MINIO_SECRET_KEY", "AzureDev123!")
    MINIO_BUCKET_UPLOADS: str = os.environ.get("MINIO_BUCKET_UPLOADS", "uploads")

    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif", "bmp", "tiff"]

    # CORS settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React development
        "http://localhost:5173",  # Vite development
        "http://frontend:3000",  # Docker container
    ]


settings = Settings()
