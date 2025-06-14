import logging
from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from app.services.auth_service import forward_to_auth_service, get_auth_service_config
from typing import Dict, Any


logger = logging.getLogger(__name__)
router = APIRouter()

# Security schemes
bearer_auth = HTTPBearer(auto_error=False)


@router.post("/login")
async def login_proxy(request: Request):
    """
    Login endpoint - forwards to auth service and return the response
    with the original status code
    """

    config = get_auth_service_config()
    result = await forward_to_auth_service("POST", "/login", request, config)

    return JSONResponse(content=result["content"], status_code=result["status_code"])


@router.post("/validate")
async def validate_proxy(request: Request):
    """
    Token validation endpoint - forwards to auth service and return the response
    with the original status code
    """

    config = get_auth_service_config()
    result = await forward_to_auth_service("POST", "/validate", request, config)

    return JSONResponse(content=result["content"], status_code=result["status_code"])


@router.get("/")
async def root() -> Dict[str, Any]:
    """Gateway information endpoint"""
    return {
        "service": "Azure API Gateway",
        "version": "1.0.0",
        "description": "FastAPI Gateway for microservices routing",
        "downstream_services": ["auth-service"],
    }
