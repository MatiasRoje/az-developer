import os


class Settings:
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("PORT", "8001"))
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development")

    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL", "postgresql://azuredev:AzureDev123!@localhost:5432/azure_dev"
    )

    RABBITMQ_URL: str = os.environ.get(
        "RABBITMQ_URL", "amqp://azuredev:AzureDev123!@localhost:5672/"
    )

    MINIO_ENDPOINT: str = os.environ.get("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY: str = os.environ.get("MINIO_ACCESS_KEY", "azuredev")
    MINIO_SECRET_KEY: str = os.environ.get("MINIO_SECRET_KEY", "AzureDev123!")
    MINIO_BUCKET_IMAGES: str = os.environ.get("MINIO_BUCKET_IMAGES", "images")
    MINIO_BUCKET_UPLOADS: str = os.environ.get("MINIO_BUCKET_UPLOADS", "uploads")

    # Image processing settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png"}
    WEBP_QUALITY: int = 80


settings = Settings()
