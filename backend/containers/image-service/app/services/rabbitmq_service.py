import logging
import json
import os
import uuid
import aio_pika
from app.core.config import settings
from app.services.minio_service import minio_service
from app.core.image_processor import image_processor
from app.db.database import create_image_record, update_image_status
from app.models.schemas import ImageRecord, ImageUploadMessage

logger = logging.getLogger(__name__)


class RabbitMQConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None

    async def connect(self):
        """Connect to RabbitMQ and setup consumer"""
        try:
            self.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
            self.channel = await self.connection.channel()

            # Set QoS to process one message at a time
            await self.channel.set_qos(prefetch_count=1)

            # Declare exchange and queue
            self.exchange = await self.channel.declare_exchange(
                "image-processing", aio_pika.ExchangeType.DIRECT, durable=True
            )

            self.upload_queue = await self.channel.declare_queue(
                "image-upload-queue", durable=True
            )

            # Bind queue to exchange
            await self.upload_queue.bind(self.exchange, "upload")

            # Start consuming messages (non-blocking)
            await self.upload_queue.consume(self.process_upload_message, no_ack=False)

            logger.info("RabbitMQ consumer connected and listening for messages")

        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    async def process_upload_message(self, message: aio_pika.IncomingMessage):
        """Process image upload message from queue"""
        async with message.process():
            try:
                message_data = json.loads(message.body.decode())
                upload_msg = ImageUploadMessage(**message_data)

                logger.info(f"Processing upload: {upload_msg.upload_id}")

                await self._create_initial_record(upload_msg)

                await self._process_image_file(upload_msg)

                logger.info(f"Successfully processed upload: {upload_msg.upload_id}")

            except Exception as e:
                logger.error(f"Failed to process upload message: {e}")
                try:
                    upload_id = json.loads(message.body.decode()).get("upload_id")
                    if upload_id:
                        await update_image_status(upload_id, "failed")
                except Exception as e:
                    logger.error(f"Failed to update image status: {e}")

    async def _create_initial_record(self, upload_msg: ImageUploadMessage):
        """Create initial database record for tracking"""
        # Generate filename for processed image
        filename = f"{uuid.uuid4()}.webp"

        image_record = ImageRecord(
            user_id=upload_msg.user_id,
            filename=filename,
            original_filename=upload_msg.original_filename,
            content_type=upload_msg.content_type,
            file_size=upload_msg.file_size,
            blob_url="",  # Will be updated after processing
            upload_status="processing",
            upload_id=upload_msg.upload_id,
        )

        await create_image_record(image_record)

    async def _process_image_file(self, upload_msg: ImageUploadMessage):
        """Process image file: convert to WebP and upload to MinIO"""
        try:
            input_file_path = await minio_service.download_file(
                settings.MINIO_BUCKET_UPLOADS,
                upload_msg.minio_object_key,
                f"tmp/{upload_msg.upload_id}",
            )

            process_result = image_processor.process_image(
                input_file_path, f"tmp/{upload_msg.upload_id}.webp"
            )

            if not process_result["success"]:
                await update_image_status(upload_msg.upload_id, "failed")
                return

            blob_url = await minio_service.upload_file(
                settings.MINIO_BUCKET_IMAGES,
                f"images/{upload_msg.upload_id}.webp",
                f"tmp/{upload_msg.upload_id}.webp",
                "image/webp",
            )

            await update_image_status(
                upload_msg.upload_id,
                "completed",
                blob_url=blob_url,
                processed_size=process_result["processed_size"],
                width=process_result["width"],
                height=process_result["height"],
                filename=f"{upload_msg.upload_id}.webp",
            )

        except Exception as e:
            logger.error(f"Image processing failed: {e}")
            await update_image_status(upload_msg.upload_id, "failed")

        finally:
            # Cleanup temporary files
            if os.path.exists(f"tmp/{upload_msg.upload_id}"):
                os.unlink(f"tmp/{upload_msg.upload_id}")
            if os.path.exists(f"tmp/{upload_msg.upload_id}.webp"):
                os.unlink(f"tmp/{upload_msg.upload_id}.webp")

            # Delete original object from upload bucket
            try:
                minio_service.client.remove_object(
                    settings.MINIO_BUCKET_UPLOADS, upload_msg.minio_object_key
                )
                logger.info(f"Deleted original object: {upload_msg.minio_object_key}")
            except Exception as e:
                logger.error(f"Failed to delete original object: {e}")

    async def close(self):
        """Close RabbitMQ connection"""
        if self.connection:
            await self.connection.close()
            logger.info("RabbitMQ consumer connection closed")


rabbitmq_consumer = RabbitMQConsumer()
