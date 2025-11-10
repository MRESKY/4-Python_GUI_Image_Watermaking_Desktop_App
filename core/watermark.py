"""
This module contains the watermarking functionality for images.
"""

from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Tuple
import logging
from .interfaces import WatermarkService as IWatermarkService
from .font_utils import get_font

logger = logging.getLogger(__name__)


class WatermarkService(IWatermarkService):
    """Service for adding watermarks to images with proper error handling."""
    
    def add_text_watermark(
        self,
        image: Image.Image,
        text: str,
        position: Tuple[int, int] = (0, 0),
        font_path: Optional[str] = None,
        font_size: int = 36,
        color: Tuple[int, int, int, int] = (255, 255, 255, 128)
    ) -> Image.Image:
        """Add text watermark to image."""
        if not isinstance(image, Image.Image):
            raise ValueError("Invalid image object provided")
        
        if not text or not text.strip():
            raise ValueError("Watermark text cannot be empty")
        
        if font_size <= 0 or font_size > 200:
            raise ValueError("Font size must be between 1 and 200")
        
        if len(color) != 4 or any(c < 0 or c > 255 for c in color):
            raise ValueError("Color must be RGBA tuple with values 0-255")
        
        try:
            # Create a copy to avoid modifying original
            result_image = image.copy()
            
            # Create watermark layer
            watermark_layer = Image.new("RGBA", result_image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark_layer)

            # Load font with better fallback system
            font = get_font(font_size, font_path)
            logger.info(f"Using font with size: {font_size}")

            # Draw text
            draw.text(position, text, font=font, fill=color)
            
            # Combine with original image
            result_image = Image.alpha_composite(result_image, watermark_layer)
            
            logger.info(f"Successfully added watermark: '{text}' at position {position}")
            return result_image
            
        except Exception as e:
            logger.error(f"Error adding watermark: {str(e)}")
            raise ValueError(f"Failed to add watermark: {str(e)}")

    def save_image(self, image: Image.Image, output_path: str) -> None:
        """Save image to file."""
        if not isinstance(image, Image.Image):
            raise ValueError("Invalid image object provided")
        
        if not output_path or not output_path.strip():
            raise ValueError("Output path cannot be empty")
        
        try:
            # Convert to RGB for JPEG compatibility
            if image.mode == "RGBA":
                # Create white background for transparency
                rgb_image = Image.new("RGB", image.size, (255, 255, 255))
                rgb_image.paste(image, mask=image.split()[-1])
            else:
                rgb_image = image.convert("RGB")
            
            # Save with high quality
            rgb_image.save(output_path, "JPEG", quality=95, optimize=True)
            logger.info(f"Successfully saved image to: {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving image to {output_path}: {str(e)}")
            raise ValueError(f"Failed to save image: {str(e)}")


class Watermarker:
    """Legacy class for backward compatibility."""
    
    def __init__(self, image_path: str):
        self.service = WatermarkService()
        try:
            self.image = Image.open(image_path).convert("RGBA")
        except Exception as e:
            raise ValueError(f"Failed to load image: {str(e)}")

    def add_text_watermark(self, text, position=(0, 0), font_path=None, font_size=36, color=(255, 255, 255, 128)):
        """Add text watermark using the legacy interface."""
        self.image = self.service.add_text_watermark(
            self.image, text, position, font_path, font_size, color
        )

    def save(self, output_path):
        """Save image using the legacy interface."""
        self.service.save_image(self.image, output_path)