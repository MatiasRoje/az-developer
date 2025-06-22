import logging
import asyncpg
from fastapi import HTTPException, status
from typing import List, Optional

from app.core.config import settings
from app.models.schemas import ImageRecord

logger = logging.getLogger(__name__)


async def init_database():
    """
    Initialize image service database tables and extensions
    This service owns the user_images table
    """
    try:
        conn = await asyncpg.connect(settings.DATABASE_URL)

        # Install required PostgreSQL extensions
        logger.info("Installing PostgreSQL extensions...")

        # Enable pgcrypto extension for UUID generation functions
        await conn.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
        logger.info("pgcrypto extension enabled")

        # Optional: Enable other useful extensions
        # UUID-OSSP for additional UUID functions (alternative to pgcrypto)
        try:
            await conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
            logger.info("uuid-ossp extension enabled")
        except Exception as e:
            logger.warning(f"uuid-ossp extension not available: {e}")

        # Create the user_images table
        logger.info("Creating user_images table...")
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_images (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id INTEGER NOT NULL,
                filename VARCHAR(255) NOT NULL,
                original_filename VARCHAR(255) NOT NULL,
                content_type VARCHAR(100) NOT NULL,
                file_size INTEGER NOT NULL,
                processed_size INTEGER,
                width INTEGER,
                height INTEGER,
                blob_url TEXT NOT NULL,
                upload_status VARCHAR(50) DEFAULT 'processing',
                upload_id UUID NOT NULL UNIQUE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """
        )

        # Create indexes for performance
        logger.info("Creating database indexes...")
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_user_images_user_id ON user_images(user_id)
        """
        )

        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_user_images_upload_id ON user_images(upload_id)
        """
        )

        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_user_images_status ON user_images(upload_status)
        """
        )

        # Verify the setup
        extension_check = await conn.fetchval(
            "SELECT COUNT(*) FROM pg_extension WHERE extname = 'pgcrypto'"
        )

        if extension_check > 0:
            logger.info("Database extensions verified successfully")
        else:
            logger.warning("pgcrypto extension verification failed")

        await conn.close()
        logger.info("Image service database initialized successfully")

    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database initialization failed",
        )


async def create_image_record(image_data: ImageRecord) -> str:
    """Create a new image record in database"""
    try:
        conn = await asyncpg.connect(settings.DATABASE_URL)

        record_id = await conn.fetchval(
            """
            INSERT INTO user_images (
                user_id, filename, original_filename, content_type,
                file_size, processed_size, width, height, blob_url,
                upload_status, upload_id
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            RETURNING id
        """,
            image_data.user_id,
            image_data.filename,
            image_data.original_filename,
            image_data.content_type,
            image_data.file_size,
            image_data.processed_size,
            image_data.width,
            image_data.height,
            image_data.blob_url,
            image_data.upload_status,
            image_data.upload_id,
        )

        await conn.close()
        logger.info(f"Created image record: {record_id}")
        return str(record_id)

    except Exception as e:
        logger.error(f"Failed to create image record: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create image record",
        )


async def get_user_images(user_id: int) -> List[ImageRecord]:
    """Get all images for a user"""
    try:
        conn = await asyncpg.connect(settings.DATABASE_URL)

        rows = await conn.fetch(
            """
            SELECT * FROM user_images
            WHERE user_id = $1
            ORDER BY created_at DESC
        """,
            user_id,
        )

        await conn.close()

        return [
            ImageRecord(
                id=str(row["id"]),
                user_id=row["user_id"],
                filename=row["filename"],
                original_filename=row["original_filename"],
                content_type=row["content_type"],
                file_size=row["file_size"],
                processed_size=row["processed_size"],
                width=row["width"],
                height=row["height"],
                blob_url=row["blob_url"],
                upload_status=row["upload_status"],
                upload_id=str(row["upload_id"]),
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
            for row in rows
        ]

    except Exception as e:
        logger.error(f"Failed to get user images: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve images",
        )


async def get_image_by_upload_id(upload_id: str) -> Optional[ImageRecord]:
    """Get image by upload_id"""
    try:
        conn = await asyncpg.connect(settings.DATABASE_URL)

        row = await conn.fetchrow(
            """
            SELECT * FROM user_images WHERE upload_id = $1
        """,
            upload_id,
        )

        await conn.close()

        if row:
            return ImageRecord(
                id=str(row["id"]),
                user_id=row["user_id"],
                filename=row["filename"],
                original_filename=row["original_filename"],
                content_type=row["content_type"],
                file_size=row["file_size"],
                processed_size=row["processed_size"],
                width=row["width"],
                height=row["height"],
                blob_url=row["blob_url"],
                upload_status=row["upload_status"],
                upload_id=str(row["upload_id"]),
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
        return None

    except Exception as e:
        logger.error(f"Failed to get image by upload_id: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve image",
        )


async def update_image_status(upload_id: str, status: str, **kwargs):
    """Update image processing status and metadata"""
    try:
        conn = await asyncpg.connect(settings.DATABASE_URL)

        # Build dynamic update query
        set_clauses = ["upload_status = $2", "updated_at = NOW()"]
        params = [upload_id, status]
        param_count = 2

        for key, value in kwargs.items():
            if value is not None:
                param_count += 1
                set_clauses.append(f"{key} = ${param_count}")
                params.append(value)

        query = f"""
            UPDATE user_images
            SET {', '.join(set_clauses)}
            WHERE upload_id = $1
        """

        await conn.execute(query, *params)
        await conn.close()

        logger.info(f"Updated image status: {upload_id} -> {status}")

    except Exception as e:
        logger.error(f"Failed to update image status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update image status",
        )
