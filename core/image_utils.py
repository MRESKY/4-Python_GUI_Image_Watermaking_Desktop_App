''' This module contains utility functions for image processing. '''

def resize_image(image, max_size):
    """Resize an image to fit within max_size while maintaining aspect ratio."""
    image.thumbnail(max_size, resample=3)
    return image