import config as config
import tkinter as tk

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
        style = config.FRAME_STYLES.copy()
        style.update(kwargs)
        super().__init__(master, **style)


class FileSelector(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.label = StyledLabel(self, text="Select File:")
        self.label.pack(side=tk.LEFT, padx=5, pady=5)
        self.entry = tk.Entry(self)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.button = StyledButton(self, text="Browse")
        self.button.pack(side=tk.RIGHT, padx=5, pady=5)

class FolderSelector(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.label = StyledLabel(self, text="Select Folder:")
        self.label.pack(side=tk.LEFT, padx=5, pady=5)
        self.entry = tk.Entry(self)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.button = StyledButton(self, text="Browse")
        self.button.pack(side=tk.RIGHT, padx=5, pady=5)

class ImagePreview(tk.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(width=config.DIMENSIONS['preview_width'],
                    height=config.DIMENSIONS['preview_height'],
                    bg=config.COLORS['surface'],
                    relief='sunken',
                    bd=2)

