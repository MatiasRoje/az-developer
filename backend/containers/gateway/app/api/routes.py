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

# Auth service routes
@router.post("/api/auth-service/login")
async def login_proxy(request: Request):
    """
    Login endpoint - forwards to auth service
    AZ-204 Pattern: API Gateway routing with service discovery
    """
    config = get_auth_service_config()
    result = await forward_to_auth_service("POST", "/login", request, config)
    return JSONResponse(content=result["content"], status_code=result["status_code"])

@router.post("/api/auth-service/validate")
async def validate_proxy(request: Request):
    """
    Token validation endpoint - forwards to auth service
    AZ-204 Pattern: Centralized authentication validation
    """
    config = get_auth_service_config()
    result = await forward_to_auth_service("POST", "/validate", request, config)
    return JSONResponse(content=result["content"], status_code=result["status_code"])

# Image service routes (to be implemented)
@router.post("/api/image-service/upload")
async def upload_image_proxy(request: Request):
    """
    Image upload endpoint - publishes to queue for async processing
    AZ-204 Pattern: Async processing with Service Bus/RabbitMQ
    """
    # TODO: Implement queue publishing logic
    return {"message": "Upload endpoint - to be implemented"}

@router.get("/api/image-service/images")
async def get_user_images_proxy(request: Request):
    """
    Get user images endpoint - returns user's uploaded images
    AZ-204 Pattern: Blob Storage integration with SAS tokens
    """
    # TODO: Implement image retrieval logic
    return {"message": "Get images endpoint - to be implemented"}

@router.get("/api/image-service/images/{image_id}")
async def get_image_details_proxy(request: Request, image_id: str):
    """
    Get specific image details
    AZ-204 Pattern: Blob Storage metadata and SAS URL generation
    """
    # TODO: Implement image details logic
    return {"message": f"Get image {image_id} details - to be implemented"}

@router.get("/")
async def root() -> Dict[str, Any]:
    """Gateway information endpoint"""
    return {
        "service": "Azure API Gateway",
        "version": "1.0.0",
        "description": "FastAPI Gateway for microservices routing",
        "downstream_services": ["auth-service", "image-service"],
        "routes": {
            "auth": ["/api/auth-service/login", "/api/auth-service/validate"],
            "image": ["/api/image-service/upload", "/api/image-service/images", "/api/image-service/images/{id}"]
        }
    }
