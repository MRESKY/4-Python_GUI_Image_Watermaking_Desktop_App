"""
Application controller that orchestrates business logic.
"""

from typing import Optional, Tuple
from PIL import Image
import logging
from .interfaces import (
    ImageProcessor, 
    WatermarkService, 
    FileDialogService,
    ImageLoadedEvent,
    WatermarkAppliedEvent,
    ImageSavedEvent,
    ErrorOccurredEvent
)

logger = logging.getLogger(__name__)


class WatermarkApplication:
    """Main application controller with business logic."""
    
    def __init__(
        self, 
        image_service: ImageProcessor,
        watermark_service: WatermarkService,
        file_dialog_service: FileDialogService,
        event_publisher=None
    ):
        self._image_service = image_service
        self._watermark_service = watermark_service
        self._file_dialog_service = file_dialog_service
        self._event_publisher = event_publisher
        
        self._current_image: Optional[Image.Image] = None
        self._original_image: Optional[Image.Image] = None
        self._image_path: Optional[str] = None
        
        logger.info("WatermarkApplication initialized")
    
    @property
    def current_image(self) -> Optional[Image.Image]:
        """Get current image."""
        return self._current_image
    
    @property
    def original_image(self) -> Optional[Image.Image]:
        """Get original image."""
        return self._original_image
    
    @property
    def has_image(self) -> bool:
        """Check if an image is loaded."""
        return self._current_image is not None
    
    @property
    def image_path(self) -> Optional[str]:
        """Get current image path."""
        return self._image_path
    
    def load_image_from_dialog(self) -> bool:
        """Load image using file dialog."""
        try:
            file_path = self._file_dialog_service.open_file_dialog()
            if not file_path:
                return False
            
            return self.load_image(file_path)
            
        except Exception as e:
            logger.error(f"Error loading image from dialog: {e}")
            self._publish_event(ErrorOccurredEvent(e, "Loading image from dialog"))
            return False
    
    def load_image(self, file_path: str) -> bool:
        """Load image from file path."""
        try:
            logger.info(f"Loading image: {file_path}")
            
            image = self._image_service.load_image(file_path)
            self._original_image = image.copy()
            self._current_image = image.copy()
            self._image_path = file_path
            
            self._publish_event(ImageLoadedEvent(file_path, image))
            logger.info("Image loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading image {file_path}: {e}")
            self._publish_event(ErrorOccurredEvent(e, f"Loading image: {file_path}"))
            return False
    
    def get_preview_image(self, max_size: Tuple[int, int]) -> Optional[Image.Image]:
        """Get resized image for preview."""
        if not self._current_image:
            return None
        
        try:
            preview = self._image_service.resize_image(self._current_image, max_size)
            return self._image_service.convert_for_display(preview)
        except Exception as e:
            logger.error(f"Error creating preview: {e}")
            return None
    
    def apply_text_watermark(
        self,
        text: str,
        position: Tuple[int, int] = None,
        font_size: int = 36,
        color: Tuple[int, int, int, int] = (255, 255, 255, 128)
    ) -> bool:
        """Apply text watermark to current image."""
        if not self._current_image:
            logger.warning("No image loaded for watermarking")
            return False
        
        try:
            if position is None:
                # Default position: bottom-right corner
                width, height = self._current_image.size
                position = (width - 200, height - 50)
            
            logger.info(f"Applying watermark: '{text}' at {position}")
            
            self._current_image = self._watermark_service.add_text_watermark(
                self._current_image, text, position, font_size=font_size, color=color
            )
            
            self._publish_event(WatermarkAppliedEvent(self._current_image, text, position))
            logger.info("Watermark applied successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error applying watermark: {e}")
            self._publish_event(ErrorOccurredEvent(e, "Applying watermark"))
            return False
    
    def reset_to_original(self) -> bool:
        """Reset current image to original."""
        if not self._original_image:
            logger.warning("No original image to reset to")
            return False
        
        try:
            self._current_image = self._original_image.copy()
            logger.info("Image reset to original")
            return True
        except Exception as e:
            logger.error(f"Error resetting image: {e}")
            return False
    
    def save_image_with_dialog(self) -> bool:
        """Save image using save dialog."""
        if not self._current_image:
            logger.warning("No image to save")
            return False
        
        try:
            file_path = self._file_dialog_service.save_file_dialog()
            if not file_path:
                return False
            
            return self.save_image(file_path)
            
        except Exception as e:
            logger.error(f"Error saving image with dialog: {e}")
            self._publish_event(ErrorOccurredEvent(e, "Saving image with dialog"))
            return False
    
    def save_image(self, output_path: str) -> bool:
        """Save current image to file path."""
        if not self._current_image:
            logger.warning("No image to save")
            return False
        
        try:
            logger.info(f"Saving image to: {output_path}")
            
            self._watermark_service.save_image(self._current_image, output_path)
            
            self._publish_event(ImageSavedEvent(output_path))
            logger.info("Image saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error saving image to {output_path}: {e}")
            self._publish_event(ErrorOccurredEvent(e, f"Saving image: {output_path}"))
            return False
    
    def clear_image(self) -> None:
        """Clear currently loaded image."""
        self._current_image = None
        self._original_image = None
        self._image_path = None
        logger.info("Image cleared")
    
    def get_image_info(self) -> dict:
        """Get information about current image."""
        if not self._current_image:
            return {}
        
        return {
            "path": self._image_path,
            "size": self._current_image.size,
            "mode": self._current_image.mode,
            "format": getattr(self._current_image, 'format', 'Unknown')
        }
    
    def _publish_event(self, event) -> None:
        """Publish an event if publisher is available."""
        if self._event_publisher:
            self._event_publisher.publish(type(event).__name__, event)