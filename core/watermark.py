''' This module contains the watermarking functionality for images. '''

from PIL import Image, ImageDraw, ImageFont

class Watermarker:
    def __init__(self, image_path):
        self.image = Image.open(image_path).convert("RGBA")

    def add_text_watermark(self, text, position=(0, 0), font_path=None, font_size=36, color=(255, 255, 255, 128)):
        watermark_layer = Image.new("RGBA", self.image.size)
        draw = ImageDraw.Draw(watermark_layer)

        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()

        draw.text(position, text, font=font, fill=color)
        combined = Image.alpha_composite(self.image, watermark_layer)
        self.image = combined

    def save(self, output_path):
        self.image.convert("RGB").save(output_path, "JPEG")