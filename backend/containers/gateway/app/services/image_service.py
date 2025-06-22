import logging
import httpx
from typing import Dict, Any, List
from fastapi import HTTPException, status
from app.core.config import settings

logger = logging.getLogger(__name__)


class ImageServiceClient:
    def __init__(self):
        self.base_url = settings.IMAGE_SERVICE_URL
        self.timeout = 30.0

    async def get_user_images(self, token: str) -> List[Dict[str, Any]]:
        """
        Get user images from image service
        AZ-204 Pattern: Direct HTTP for fast read operations
        """
        try:
            headers = {"Authorization": f"Bearer {token}"}

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/images", headers=headers)

                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(
                        f"Image service error: {response.status_code} - {response.text}"
                    )
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Image service error: {response.text}",
                    )

        except httpx.TimeoutException:
            logger.error("Image service timeout")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Image service timeout",
            )
        except Exception as e:
            logger.error(f"Failed to get user images: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to communicate with image service",
            )

    async def get_image_details(self, image_id: str, token: str) -> Dict[str, Any]:
        """
        Get specific image details from image service
        AZ-204 Pattern: Direct HTTP for metadata retrieval
        """
        try:
            headers = {"Authorization": f"Bearer {token}"}

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/images/{image_id}/status", headers=headers
                )

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
                    )
                else:
                    logger.error(
                        f"Image service error: {response.status_code} - {response.text}"
                    )
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Image service error: {response.text}",
                    )

        except httpx.TimeoutException:
            logger.error("Image service timeout")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Image service timeout",
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get image details: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to communicate with image service",
            )


# Global instance
image_service_client = ImageServiceClient()
