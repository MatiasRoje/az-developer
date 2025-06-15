import os


class Settings:
    JWT_SECRET: str = os.environ.get(
        "JWT_SECRET", "your-super-secret-jwt-key-change-in-production"
    )
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("PORT", "8000"))
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development")
    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL", 
        "postgresql://azuredev:AzureDev123!@localhost:5432/azure_dev"
    )

    @classmethod
    def get_jwt_secret(cls) -> str:
        if not cls.JWT_SECRET:
            raise ValueError("JWT_SECRET environment variable is required")
        return cls.JWT_SECRET


settings = Settings()
