"""
Font utilities for better watermark text rendering.
"""

from PIL import ImageFont
import logging
import os

logger = logging.getLogger(__name__)


def get_font(font_size: int, font_path: str = None):
    """
    Get a font with the specified size, trying multiple fallback options.
    """
    
    # Try user-specified font first
    if font_path:
        try:
            font = ImageFont.truetype(font_path, font_size)
            logger.info(f"Using custom font: {font_path} with size {font_size}")
            return font
        except (OSError, IOError) as e:
            logger.warning(f"Could not load custom font {font_path}: {e}")
    
    # Try common system fonts with the specified size
    system_fonts = [
        # Windows fonts
        'arial.ttf',
        'Arial.ttf', 
        'calibri.ttf',
        'Calibri.ttf',
        'times.ttf',
        'Times.ttf',
        # Cross-platform fonts
        'helvetica.ttf',
        'Helvetica.ttf',
        'DejaVuSans.ttf',
        'LiberationSans-Regular.ttf',
        # macOS fonts
        '/System/Library/Fonts/Arial.ttf',
        '/System/Library/Fonts/Helvetica.ttf',
        # Linux fonts
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/TTF/arial.ttf'
    ]
    
    for font_name in system_fonts:
        try:
            font = ImageFont.truetype(font_name, font_size)
            logger.info(f"Using system font: {font_name} with size {font_size}")
            return font
        except (OSError, IOError):
            continue
    
    # If no TTF font found, create a larger default font by scaling
    try:
        # Try to use default font multiple times to simulate larger size
        default_font = ImageFont.load_default()
        logger.warning(f"Using default font. Requested size: {font_size} (size cannot be controlled)")
        return default_font
    except Exception as e:
        logger.error(f"Could not load any font: {e}")
        return ImageFont.load_default()


def download_font_suggestion():
    """
    Provide suggestion for downloading fonts for better watermark quality.
    """
    suggestion = """
    For better watermark quality with custom font sizes, consider:
    
    1. Download a free font like 'Roboto' or 'Open Sans'
    2. Place it in a 'fonts' folder in your project
    3. Use the font path in watermark settings
    
    Good free fonts:
    - Roboto: https://fonts.google.com/specimen/Roboto
    - Open Sans: https://fonts.google.com/specimen/Open+Sans
    - Arial (often pre-installed on Windows)
    """
    return suggestion