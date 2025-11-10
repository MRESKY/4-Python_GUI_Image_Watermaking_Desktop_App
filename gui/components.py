import gui.config as config
import tkinter as tk
from tkinter import filedialog


class StyledButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        style = config.BUTTON_STYLE.copy()
        style.update(kwargs)
        super().__init__(master, **style)

class StyledInput(tk.Entry):
    def __init__(self, master=None, **kwargs):
        style = config.INPUT_STYLE.copy()
        style.update(kwargs)
        super().__init__(master, **style)

class StyledLabel(tk.Label):
    def __init__(self, master=None, **kwargs):
        style = config.LABEL_STYLE.copy()
        style.update(kwargs)
        super().__init__(master, **style)

class StyledFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        style = config.FRAME_STYLE.copy()
        style.update(kwargs)
        super().__init__(master, **style)


class FileSelector(tk.Frame):
    def __init__(self, master=None, select_folder=False):
        super().__init__(master)
        self.select_folder = select_folder
        self.path_var = tk.StringVar()

        self.label = StyledLabel(self, text="Select File:")
        self.label.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.entry = StyledInput(self, textvariable=self.path_var)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        self.button = StyledButton(self, text="Browse", command=self.browse)
        self.button.pack(side=tk.RIGHT, padx=5, pady=5)

    def browse(self):
        if self.select_folder:
            path = filedialog.askdirectory(title="Select Folder")
        else:
            path = filedialog.askopenfilename(
                title="Select File",
                filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All Files", "*.*")]
            )

        if path:
            self.path_var.set(path)
    
    def get_path(self):
        return self.path_var.get()

class ImagePreview(tk.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(width=config.DIMENSIONS['preview_width'],
                    height=config.DIMENSIONS['preview_height'],
                    bg=config.COLORS['surface'],
                    relief='sunken',
                    bd=2)

