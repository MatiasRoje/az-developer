import os


class Settings:
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("PORT", "8080"))
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development")
    
    # CORS origins (comma-separated)
    CORS_ORIGINS: str = os.environ.get(
        "CORS_ORIGINS", 
        "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:3000"
    )
    
    # RabbitMQ connection
    RABBITMQ_URL: str = os.environ.get(
        "RABBITMQ_URL",
        "amqp://azuredev:AzureDev123!@localhost:5672/"
    )
    
    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()
