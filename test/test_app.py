"""
Test script to verify application works.
"""

import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    # Test imports
    print("Testing imports...")
    
    from core.interfaces import ImageProcessor, WatermarkService, FileDialogService
    print("✓ Core interfaces imported")
    
    from core.image_utils import ImageService
    print("✓ Image service imported")
    
    from core.watermark import WatermarkService as WatermarkServiceImpl
    print("✓ Watermark service imported")
    
    from core.container import ServiceContainer
    print("✓ Service container imported")
    
    from core.application import WatermarkApplication
    print("✓ Application controller imported")
    
    from gui.services import FileDialogService as FileDialogServiceImpl
    print("✓ File dialog service imported")
    
    print("\nAll core imports successful!")
    
    # Test service container setup
    print("\nTesting service container...")
    
    container = ServiceContainer()
    container.register_singleton(ImageProcessor, ImageService)
    container.register_singleton(WatermarkService, WatermarkServiceImpl)
    container.register_singleton(FileDialogService, FileDialogServiceImpl)
    
    # Test getting services
    image_service = container.get(ImageProcessor)
    watermark_service = container.get(WatermarkService)
    file_service = container.get(FileDialogService)
    
    print("✓ Services created successfully")
    
    # Test application controller
    app = WatermarkApplication(image_service, watermark_service, file_service)
    print("✓ Application controller created")
    
    print("\n🎉 All tests passed! Application setup is working correctly.")
    
except Exception as e:
    print(f"\n❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)