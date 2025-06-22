import logging
from minio import Minio
from minio.error import S3Error
from app.core.config import settings
import io

logger = logging.getLogger(__name__)


class MinIOService:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT.replace("http://", ""),
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False,  # True for HTTPS
        )
        self.bucket_name = settings.MINIO_BUCKET_UPLOADS

    async def upload_image(
        self, file_data: bytes, object_key: str, content_type: str
    ) -> str:
        """Upload image to MinIO and return object key"""
        try:
            # Ensure bucket exists
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)

            # Upload file
            self.client.put_object(
                self.bucket_name,
                object_key,
                io.BytesIO(file_data),
                length=len(file_data),
                content_type=content_type,
            )

            logger.info(f"Uploaded to MinIO: {object_key}")
            return object_key

        except S3Error as e:
            logger.error(f"MinIO upload failed: {e}")
            raise


# Global instance
minio_service = MinIOService()
