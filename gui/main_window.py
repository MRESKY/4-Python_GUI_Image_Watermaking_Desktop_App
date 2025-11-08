''' This module contains the main window for the image watermarking application. '''

from tkinter import Tk
import config as config
import components as components


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Watermarking Application")
        self.geometry(f"{config.DIMENSIONS['window_width']}x{config.DIMENSIONS['window_height']}")
        self.configure(bg=config.COLORS['background'])
    
    def run(self):
        self.mainloop()


class WindowProcessing(MainWindow):
    def __init__(self, mode='mono'):
        super().__init__()
        self.mode = mode
        title = "Mono Watermarking" if mode == 'mono' else "Batch Watermarking"
        self.title(f'Image Watermarking - {title}')
        self.file_selector = components.FileSelector(self)
        self.file_selector.pack(padx=10, pady=10)
        self.image_preview = components.ImagePreview(self)
        self.image_preview.pack(padx=10, pady=10)

class HomeWindow(MainWindow):
    def __init__(self):
        super().__init__()
        self.label = components.StyledLabel(self, text="Welcome to the Image Watermarking Application")
        self.label.pack(padx=20, pady=20)
        self.label2 = components.StyledLabel(self, text="Select your Mono or Batch Watermarking option")
        self.label2.pack(padx=20, pady=20)

        self.mono_button = components.StyledButton(self, text="Mono Watermarking", command=self.mono_watermarking)
        self.mono_button.pack(padx=10, pady=10)
        self.batch_button = components.StyledButton(self, text="Batch Watermarking", command=self.batch_watermarking)
        self.batch_button.pack(padx=10, pady=10)

    def mono_watermarking(self):
        self.destroy()
        mono_window = WindowProcessing()
        mono_window.run()

    def batch_watermarking(self):
        self.destroy()
        batch_window = WindowProcessing()
        batch_window.run()


if __name__ == "__main__":
    app = HomeWindow()
    app.run()