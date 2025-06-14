import os


class Settings:
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("PORT", "8080"))
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development")


settings = Settings()
