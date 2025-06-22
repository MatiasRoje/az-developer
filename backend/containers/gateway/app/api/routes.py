import logging
from datetime import datetime, timezone
import uuid
from fastapi import Request, APIRouter, UploadFile, File, HTTPException, status, Header
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from app.services.auth_service import (
    forward_to_auth_service,
    get_auth_service_config,
    validate_token_only,
)
from app.services.rabbitmq_service import rabbitmq_service
from app.services.image_service import image_service_client
from app.services.minio_service import minio_service
from app.core.config import settings
from typing import Optional

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
    response = await forward_to_auth_service("POST", "/login", request, config)
    return JSONResponse(
        status_code=response["status_code"],
        content=response["content"],
        headers=dict(response["headers"]),
    )


@router.post("/api/auth-service/validate")
async def validate_proxy(request: Request):
    """
    Token validation endpoint - forwards to auth service
    AZ-204 Pattern: Centralized authentication validation
    """
    config = get_auth_service_config()
    response = await forward_to_auth_service("POST", "/validate", request, config)
    return JSONResponse(
        status_code=response["status_code"],
        content=response["content"],
        headers=dict(response["headers"]),
    )


# Image service routes
@router.post("/api/image-service/upload")
async def upload_image_proxy(
    file: UploadFile = File(...), authorization: Optional[str] = Header(None)
):
    """
    Image upload endpoint - validates token and publishes to queue
    AZ-204 Pattern: Async processing with Service Bus (RabbitMQ locally)
    """
    try:
        # Validate token using header-only validation (avoids stream consumption issue)
        config = get_auth_service_config()
        user_info = await validate_token_only(authorization, config)
        logger.info(f"DEBUG: user_info: {user_info}")
        user_id = user_info.get("id")
        logger.info(f"DEBUG: extracted user_id: {user_id}")

        # Validate file type
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="File name is required"
            )

        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Supported: {settings.ALLOWED_EXTENSIONS}",
            )

        # Validate file size
        file_size = 0
        content = await file.read()
        file_size = len(content)

        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Max size: {settings.MAX_FILE_SIZE} bytes",
            )

        # Generate unique upload ID
        upload_id = str(uuid.uuid4())

        # Upload file to MinIO
        uploaded_key = await minio_service.upload_image(
            content, upload_id, file.content_type
        )

        # Publish to RabbitMQ queue
        message = {
            "upload_id": upload_id,
            "user_id": user_id,
            "original_filename": file.filename,
            "content_type": file.content_type,
            "file_size": file_size,
            "minio_object_key": uploaded_key,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        await rabbitmq_service.publish_image_upload_message(message)

        logger.info(f"Image upload queued: {upload_id} for user {user_id}")

        return {
            "message": "Image upload queued for processing",
            "upload_id": upload_id,
            "status": "queued",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in upload: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Upload processing error",
        )


@router.get("/api/image-service/images")
async def get_user_images_proxy(authorization: Optional[str] = Header(None)):
    """
    Get user images - validates token and calls image service directly
    AZ-204 Pattern: Direct HTTP for fast read operations
    """
    # Validate token
    config = get_auth_service_config()
    await validate_token_only(authorization, config)

    # Get images from image service
    images = await image_service_client.get_user_images(authorization)

    return {"images": images, "count": len(images)}


@router.get("/api/image-service/images/{image_id}")
async def get_image_proxy(image_id: str, authorization: Optional[str] = Header(None)):
    """
    Get specific image - validates token and calls image service directly
    AZ-204 Pattern: Direct HTTP for fast read operations
    """
    # Validate token
    config = get_auth_service_config()
    await validate_token_only(authorization, config)

    # Get image from image service
    image = await image_service_client.get_image(image_id, authorization)

    return image


# Health check endpoint
@router.get("/")
async def health_check():
    """
    Health check endpoint
    AZ-204 Pattern: Container health monitoring
    """
    return {"service": "Azure Gateway", "status": "healthy", "version": "1.0.0"}
