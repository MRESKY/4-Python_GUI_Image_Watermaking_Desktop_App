"""
This module defines interfaces/protocols for dependency injection.
"""

from abc import ABC, abstractmethod
from typing import Protocol, Optional, Tuple, List
from PIL import Image


class ImageProcessor(Protocol):
    """Protocol for image processing operations."""
    
    def load_image(self, path: str) -> Image.Image:
        """Load an image from file path."""
        ...
    
    def resize_image(self, image: Image.Image, max_size: Tuple[int, int]) -> Image.Image:
        """Resize an image while maintaining aspect ratio."""
        ...
    
    def convert_for_display(self, image: Image.Image) -> Image.Image:
        """Convert image for display in GUI."""
        ...


class WatermarkService(Protocol):
    """Protocol for watermarking operations."""
    
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
        ...
    
    def save_image(self, image: Image.Image, output_path: str) -> None:
        """Save image to file."""
        ...


class FileDialogService(Protocol):
    """Protocol for file dialog operations."""
    
    def open_file_dialog(self, file_types: List[Tuple[str, str]]) -> Optional[str]:
        """Show file open dialog and return selected path."""
        ...
    
    def save_file_dialog(
        self, 
        default_extension: str, 
        file_types: List[Tuple[str, str]]
    ) -> Optional[str]:
        """Show file save dialog and return selected path."""
        ...
    
    def open_folder_dialog(self) -> Optional[str]:
        """Show folder selection dialog and return selected path."""
        ...


class EventPublisher(Protocol):
    """Protocol for event publishing."""
    
    def subscribe(self, event_type: str, handler) -> None:
        """Subscribe to an event type."""
        ...
    
    def unsubscribe(self, event_type: str, handler) -> None:
        """Unsubscribe from an event type."""
        ...
    
    def publish(self, event_type: str, data=None) -> None:
        """Publish an event with optional data."""
        ...


# Domain Events
class ImageLoadedEvent:
    """Event fired when an image is loaded."""
    def __init__(self, image_path: str, image: Image.Image):
        self.image_path = image_path
        self.image = image


class WatermarkAppliedEvent:
    """Event fired when watermark is applied."""
    def __init__(self, image: Image.Image, text: str, position: Tuple[int, int]):
        self.image = image
        self.text = text
        self.position = position


class ImageSavedEvent:
    """Event fired when image is saved."""
    def __init__(self, output_path: str):
        self.output_path = output_path


class ErrorOccurredEvent:
    """Event fired when an error occurs."""
    def __init__(self, error: Exception, context: str = ""):
        self.error = error
        self.context = context