"""
This module contains utility functions and services for image processing.
"""

from typing import Tuple
from PIL import Image
import logging
from .interfaces import ImageProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageService(ImageProcessor):
    """Service for image processing operations with proper error handling."""
    
    def load_image(self, path: str) -> Image.Image:
        """Load an image from file path."""
        try:
            logger.info(f"Loading image from: {path}")
            image = Image.open(path).convert("RGBA")
            logger.info(f"Successfully loaded image: {image.size}")
            return image
        except FileNotFoundError:
            logger.error(f"Image file not found: {path}")
            raise ValueError(f"Image file not found: {path}")
        except Exception as e:
            logger.error(f"Error loading image {path}: {str(e)}")
            raise ValueError(f"Failed to load image: {str(e)}")
    
    def resize_image(self, image: Image.Image, max_size: Tuple[int, int]) -> Image.Image:
        """Resize an image to fit within max_size while maintaining aspect ratio."""
        if not isinstance(image, Image.Image):
            raise ValueError("Invalid image object provided")
        
        if not max_size or len(max_size) != 2 or any(dim <= 0 for dim in max_size):
            raise ValueError("Invalid max_size provided. Must be tuple of positive integers.")
        
        try:
            # Create a copy to avoid modifying original
            image_copy = image.copy()
            original_size = image_copy.size
            
            # Calculate new size maintaining aspect ratio
            image_copy.thumbnail(max_size, Image.Resampling.LANCZOS)
            new_size = image_copy.size
            
            logger.info(f"Resized image from {original_size} to {new_size}")
            return image_copy
            
        except Exception as e:
            logger.error(f"Error resizing image: {str(e)}")
            raise ValueError(f"Failed to resize image: {str(e)}")
    
    def convert_for_display(self, image: Image.Image) -> Image.Image:
        """Convert image for display in GUI."""
        try:
            if image.mode == "RGBA":
                # Create white background for transparency
                background = Image.new("RGB", image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])  # Use alpha channel as mask
                return background
            else:
                return image.convert("RGB")
        except Exception as e:
            logger.error(f"Error converting image for display: {str(e)}")
            raise ValueError(f"Failed to convert image: {str(e)}")


def resize_image(image: Image.Image, max_size: Tuple[int, int]) -> Image.Image:
    """Legacy function for backward compatibility."""
    service = ImageService()
    return service.resize_image(image, max_size)