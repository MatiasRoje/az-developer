from pydantic import BaseModel


class ServiceConfig(BaseModel):
    """Configuration for downstream services"""

    auth_service_url: str
    timeout: int = 30
