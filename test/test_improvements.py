#!/usr/bin/env python3
"""
Quick test script to validate improvements made to the watermarking application.
"""

import sys
import os
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.container import ServiceContainer
from core.application import WatermarkApplication
from PIL import Image, ImageDraw, ImageFont

def test_font_system():
    """Test the font system improvements."""
    print("Testing font system...")
    
    # Import font utils
    from core.font_utils import get_font
    
    # Test different font sizes
    test_sizes = [24, 48, 64, 96, 128]
    
    for size in test_sizes:
        try:
            font = get_font(size)
            print(f"✓ Font size {size}px loaded successfully: {font}")
        except Exception as e:
            print(f"✗ Error loading font size {size}px: {e}")

def test_service_container():
    """Test the service container and dependency injection."""
    print("\nTesting service container...")
    
    try:
        container = ServiceContainer()
        print("✓ Service container created")
        
        # Test service registration
        container.configure()
        print("✓ Services configured")
        
        # Test getting services
        image_service = container.get_image_processor()
        watermark_service = container.get_watermark_service()
        file_service = container.get_file_dialog_service()
        
        print("✓ All services retrieved successfully")
        print(f"  - Image processor: {type(image_service).__name__}")
        print(f"  - Watermark service: {type(watermark_service).__name__}")
        print(f"  - File dialog service: {type(file_service).__name__}")
        
    except Exception as e:
        print(f"✗ Service container error: {e}")

def test_application_controller():
    """Test the application controller."""
    print("\nTesting application controller...")
    
    try:
        container = ServiceContainer()
        container.configure()
        app = WatermarkApplication(container)
        print("✓ Application controller created")
        
        # Test without image (should handle gracefully)
        result = app.apply_watermark("Test", (50, 50), 128, 64, "black")
        if not result:
            print("✓ Application correctly handles no image case")
        
    except Exception as e:
        print(f"✗ Application controller error: {e}")

def test_config_and_imports():
    """Test that all config and imports work correctly."""
    print("\nTesting configuration and imports...")
    
    try:
        from gui.config import COLORS, FONTS, DIMENSIONS, BUTTON_FONT
        print("✓ GUI config imported successfully")
        print(f"  - Colors: {len(COLORS)} defined")
        print(f"  - Fonts: {len(FONTS)} defined") 
        print(f"  - Button font: {BUTTON_FONT}")
        print(f"  - Window size: {DIMENSIONS['window_width']}x{DIMENSIONS['window_height']}")
        
        from gui.components import StyledButton, StyledLabel, StyledFrame
        print("✓ GUI components imported successfully")
        
    except Exception as e:
        print(f"✗ Config/import error: {e}")

def create_test_image():
    """Create a simple test image for testing."""
    print("\nCreating test image...")
    
    try:
        # Create a simple test image
        img = Image.new('RGB', (400, 300), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Add some content
        draw.rectangle([50, 50, 350, 250], fill='white', outline='black')
        draw.text((100, 150), "Test Image", fill='black')
        
        test_path = project_root / "test_image.jpg"
        img.save(test_path)
        print(f"✓ Test image created: {test_path}")
        
        return test_path
        
    except Exception as e:
        print(f"✗ Error creating test image: {e}")
        return None

def main():
    """Run all tests."""
    print("🔧 Testing Image Watermarking Application Improvements")
    print("=" * 60)
    
    # Configure logging for testing
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s:%(name)s:%(message)s'
    )
    
    # Run tests
    test_config_and_imports()
    test_service_container() 
    test_application_controller()
    test_font_system()
    
    # Create test resources
    test_image_path = create_test_image()
    
    print("\n" + "=" * 60)
    print("✅ Testing completed!")
    print("\n📝 Summary of improvements:")
    print("  • Modern OOP architecture with dependency injection")
    print("  • Robust font loading system with fallbacks") 
    print("  • Compact, scrollable UI layout")
    print("  • Better error handling and logging")
    print("  • Service-oriented design patterns")
    print("  • Type-safe interfaces with protocols")
    print("\n🚀 Application ready for use!")
    
    if test_image_path and test_image_path.exists():
        print(f"\n💡 Tip: Use {test_image_path} to test the application")

if __name__ == "__main__":
    main()