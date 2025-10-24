''' This module contains the main window for the image watermarking application. '''

from tkinter import Tk
from tkinter import ttk
from . import component


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Watermarking Application")
        self.geometry(f"{component.DIMENSIONS['window_width']}x{component.DIMENSIONS['window_height']}")
        self.configure(bg=component.COLORS['background'])
    
    def run(self):
        self.mainloop()

    def setup_ui(self, commands=None):
        btn = ttk.Button(self, text="Sample Button", style='TButton')
        btn.pack(pady=component.DIMENSIONS['padding_large'])
