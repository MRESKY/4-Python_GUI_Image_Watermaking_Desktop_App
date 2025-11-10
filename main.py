"""
Main entry point for the Image Watermarking Application.

This module sets up dependency injection and starts the application.
"""

import logging
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.container import ServiceContainer
from core.interfaces import ImageProcessor, WatermarkService, FileDialogService
from core.image_utils import ImageService
from core.watermark import WatermarkService as WatermarkServiceImpl
from core.application import WatermarkApplication
from gui.services import FileDialogService as FileDialogServiceImpl
from gui.main_window import MainWindow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def configure_services() -> ServiceContainer:
    """Configure and register all application services."""
    container = ServiceContainer()
    
    # Register core services as singletons
    container.register_singleton(ImageProcessor, ImageService)
    container.register_singleton(WatermarkService, WatermarkServiceImpl)
    container.register_singleton(FileDialogService, FileDialogServiceImpl)
    
    # Register application controller
    container.register_factory(
        WatermarkApplication,
        lambda: WatermarkApplication(
            container.get(ImageProcessor),
            container.get(WatermarkService),
            container.get(FileDialogService)
        )
    )
    
    logger.info("Services configured successfully")
    return container


def main():
    """Main entry point."""
    try:
        logger.info("Starting Image Watermarking Application")
        
        # Setup dependency injection
        container = configure_services()
        
        # Create application controller
        app_controller = container.get(WatermarkApplication)
        
        # Create and run GUI
        gui = MainWindow(app_controller)
        gui.run()
        
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        import traceback
        traceback.print_exc()
    finally:
        logger.info("Application shutting down")


if __name__ == "__main__":
    main()