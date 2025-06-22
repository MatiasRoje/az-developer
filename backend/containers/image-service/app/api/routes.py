import logging
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from typing import List

from app.core.config import settings
from app.db.database import get_user_images, get_image_by_upload_id
from app.models.schemas import ImageResponse, UploadStatusResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# Security scheme
bearer_auth = HTTPBearer()


def extract_user_from_token(token: str) -> str:
    """
    Extract user ID from JWT token
    In production, you'd validate the token signature
    """
    try:
        import json
        import base64

        # Decode JWT payload (skip signature validation for demo)
        payload = json.loads(base64.b64decode(token.split(".")[1] + "=="))
        return payload.get("id", payload.get("id", "unknown"))
    except Exception as e:
        logger.error(f"Token extraction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


@router.get("/images", response_model=List[ImageResponse])
async def get_user_images_endpoint(token=Depends(bearer_auth)):
    """
    Get all images for the authenticated user
    AZ-204 Pattern: Direct HTTP for fast read operations
    """
    try:
        user_id = extract_user_from_token(token.credentials)

        # Get images from database
        images = await get_user_images(user_id)

        # Convert to response format
        return [
            ImageResponse(
                id=img.id,
                filename=img.filename,
                original_filename=img.original_filename,
                file_size=img.file_size,
                processed_size=img.processed_size,
                width=img.width,
                height=img.height,
                blob_url=img.blob_url,
                upload_status=img.upload_status,
                created_at=img.created_at,
            )
            for img in images
        ]

    except Exception as e:
        logger.error(f"Failed to get user images: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve images",
        )


@router.get("/images/{upload_id}/status", response_model=UploadStatusResponse)
async def get_upload_status(upload_id: str, token=Depends(bearer_auth)):
    """
    Get upload status for a specific image
    AZ-204 Pattern: Status polling for async operations
    """
    try:
        user_id = extract_user_from_token(token.credentials)

        image = await get_image_by_upload_id(upload_id)

        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Upload not found"
            )

        if image.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )

        response = UploadStatusResponse(
            upload_id=upload_id,
            status=image.upload_status,
            message=f"Upload is {image.upload_status}",
        )

        if image.upload_status == "completed":
            response.image = ImageResponse(
                id=image.id,
                filename=image.filename,
                original_filename=image.original_filename,
                file_size=image.file_size,
                processed_size=image.processed_size,
                width=image.width,
                height=image.height,
                blob_url=image.blob_url,
                upload_status=image.upload_status,
                created_at=image.created_at,
            )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get upload status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get upload status",
        )


@router.get("/")
async def root():
    """Image service information endpoint"""
    return {
        "service": "Azure Image Microservice",
        "version": "1.0.0",
        "description": "Image processing service for AZ-204",
        "status": "running",
        "supported_formats": list(settings.ALLOWED_EXTENSIONS),
        "max_file_size_mb": settings.MAX_FILE_SIZE // (1024 * 1024),
    }
