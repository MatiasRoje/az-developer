import os
from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi import status
from typing import Dict, Any
import httpx
from app.models.schemas import ServiceConfig
import logging

logger = logging.getLogger(__name__)


def get_auth_service_config() -> ServiceConfig:
    """
    AZ-204 Exam Note: In production, use Azure Service Discovery
    - Azure Container Apps: Built-in service discovery
    - AKS: Kubernetes service discovery
    - API Management: Backend service configuration
    """
    return ServiceConfig(
        auth_service_url=os.environ.get("AUTH_SERVICE_URL", "http://localhost:8000"),
        timeout=int(os.environ.get("AUTH_SERVICE_TIMEOUT", "30")),
    )


async def forward_to_auth_service(
    method: str, path: str, request: Request, config: ServiceConfig
) -> Dict[str, Any]:
    """
    Forward requests to auth service with proper error handling
    AZ-204 Pattern: Microservice communication with circuit breaker concepts
    """

    # Prepare headers for forwarding
    headers = dict(request.headers)

    # Remove host header to avoid conflicts
    headers.pop("host", None)

    # Construct target URL
    target_url = f"{config.auth_service_url}{path}"

    try:
        async with httpx.AsyncClient(timeout=config.timeout) as client:

            if method == "GET":
                response = await client.get(target_url, headers=headers)
            elif method == "POST":
                # Get request body for POST requests
                body = await request.body()
                response = await client.post(target_url, headers=headers, content=body)
            else:
                raise HTTPException(
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                    detail=f"Method {method} not supported",
                )

            logger.info(
                f"Forwarded {method} {path} to auth-service: {response.status_code}"
            )

            return {
                "status_code": response.status_code,
                "content": (
                    response.json()
                    if response.headers.get("content-type", "").startswith(
                        "application/json"
                    )
                    else response.text
                ),
                "headers": dict(response.headers),
            }

    except httpx.TimeoutException:
        logger.error(f"Timeout forwarding to auth-service: {target_url}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="Auth service timeout"
        )
    except httpx.RequestError as e:
        logger.error(f"Request error forwarding to auth-service: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Auth service unavailable",
        )
    except Exception as e:
        logger.error(f"Unexpected error forwarding to auth-service: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gateway internal error",
        )
