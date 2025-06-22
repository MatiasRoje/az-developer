import logging
import json
from typing import Dict, Any
import aio_pika
from aio_pika import Message
from app.core.config import settings

logger = logging.getLogger(__name__)


class RabbitMQService:
    def __init__(self):
        self.connection = None
        self.channel = None

    async def connect(self):
        """
        Connect to RabbitMQ
        AZ-204 Pattern: Message queue connection management
        """
        try:
            self.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
            self.channel = await self.connection.channel()

            # Declare exchanges and queues
            await self._setup_queues()

            logger.info("Connected to RabbitMQ successfully")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    async def _setup_queues(self):
        """
        Setup RabbitMQ exchanges and queues for image processing
        AZ-204 Pattern: Message queue topology setup
        """
        # Declare exchange
        self.exchange = await self.channel.declare_exchange(
            "image-processing", aio_pika.ExchangeType.DIRECT, durable=True
        )

        # Declare queues
        self.image_upload_queue = await self.channel.declare_queue(
            "image-upload-queue", durable=True
        )

        # Bind queues to exchange
        await self.image_upload_queue.bind(self.exchange, "upload")

        logger.info("RabbitMQ queues setup completed")

    async def publish_image_upload_message(self, message_data: Dict[str, Any]):
        """
        Publish image upload message to queue
        AZ-204 Pattern: Async message publishing
        """
        try:
            message = Message(
                json.dumps(message_data).encode(),
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            )

            await self.exchange.publish(message, routing_key="upload")

            logger.info(
                f"Published image upload message: {message_data.get('upload_id')}"
            )

        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise

    async def close(self):
        """Close RabbitMQ connection"""
        if self.connection:
            await self.connection.close()
            logger.info("RabbitMQ connection closed")


# Global instance
rabbitmq_service = RabbitMQService()
