from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ImageUploadMessage(BaseModel):
    """Message schema for image upload queue"""

    upload_id: str
    user_id: int
    original_filename: str
    content_type: str
    file_size: int
    minio_object_key: str
    timestamp: str


class ImageRecord(BaseModel):
    """Image metadata model for database"""

    id: Optional[str] = None
    user_id: int
    filename: str
    original_filename: str
    content_type: str
    file_size: int
    processed_size: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    blob_url: str
    upload_status: str = "processing"
    upload_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ImageResponse(BaseModel):
    """API response for image data"""

    id: str
    filename: str
    original_filename: str
    file_size: int
    processed_size: Optional[int]
    width: Optional[int]
    height: Optional[int]
    blob_url: str
    upload_status: str
    created_at: datetime


class UploadStatusResponse(BaseModel):
    """Response for upload status check"""

    upload_id: str
    status: str
    message: str
    image: Optional[ImageResponse] = None
