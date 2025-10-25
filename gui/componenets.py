import gui.config as config
import tkinter as tk

class StyledButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        style = config.BUTTON_STYLES.copy()
        style.update(kwargs)
        super().__init__(master, **style)


class StyledLabel(tk.Label):
    def __init__(self, master=None, **kwargs):
        style = config.LABEL_STYLES.copy()
        style.update(kwargs)
        super().__init__(master, **style)

