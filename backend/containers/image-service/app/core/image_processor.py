import logging
import os
from PIL import Image
from app.core.config import settings

logger = logging.getLogger(__name__)


class ImageProcessor:

    @staticmethod
    def process_image(input_path: str, output_path: str) -> dict:
        """Convert image to WebP and extract metadata"""
        try:
            with Image.open(input_path) as img:
                width, height = img.size

                if img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGB")

                img.save(
                    output_path, "WEBP", quality=settings.WEBP_QUALITY, optimize=True
                )

                processed_size = os.path.getsize(output_path)

                return {
                    "width": width,
                    "height": height,
                    "processed_size": processed_size,
                    "success": True,
                }

        except Exception as e:
            logger.error(f"Image processing failed: {e}")
            return {"success": False, "error": str(e)}


image_processor = ImageProcessor()
