import logging
from minio import Minio
from minio.error import S3Error
from app.core.config import settings

logger = logging.getLogger(__name__)


class MinIOService:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT.replace("http://", ""),
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False,  # Set to True for HTTPS
        )

    async def upload_file(
        self, bucket_name: str, object_name: str, file_path: str, content_type: str
    ):
        """Upload file to MinIO"""
        try:
            # Ensure bucket exists
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)

            # Upload file
            self.client.fput_object(
                bucket_name, object_name, file_path, content_type=content_type
            )

            # Generate URL
            # NOTE: Harcoded as the MINIO_ENDPOINT is only working in the docker network and it's not accessible from the browser
            url = f"http://localhost:9000/{bucket_name}/{object_name}"
            logger.info(f"Uploaded file to MinIO: {url}")
            return url

        except S3Error as e:
            logger.error(f"MinIO upload error: {e}")
            raise Exception(f"Failed to upload to MinIO: {e}")

    def get_file_url(self, bucket_name: str, object_name: str) -> str:
        """Get public URL for file"""
        return f"http://{settings.MINIO_ENDPOINT}/{bucket_name}/{object_name}"

    async def download_file(
        self, bucket_name: str, object_name: str, output_location: str
    ) -> bytes:
        """Download file from MinIO to an output location"""
        try:
            self.client.fget_object(bucket_name, object_name, output_location)
            return output_location
        except S3Error as e:
            logger.error(f"MinIO download error: {e}")
            raise Exception(f"Failed to download from MinIO: {e}")


minio_service = MinIOService()
