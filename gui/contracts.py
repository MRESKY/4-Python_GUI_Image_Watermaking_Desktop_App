from typing import Protocol, TypedDict

# Define protocols and typed dictionaries for GUI configuration

class ColorPalette(TypedDict):
    primary: str
    secondary: str
    accent: str
    background: str
    surface: str
    text: str
    text_secondary: str
    success: str
    warning: str
    error: str

class FontStyle(Protocol):
    title: tuple[str, int, str]
    header: tuple[str, int, str]
    body: tuple[str, int]
    small: tuple[str, int]
    button: tuple[str, int, str]

class DimensionSettings(Protocol):
    window_width: int
    window_height: int
    preview_width: int
    preview_height: int
    button_height: int
    padding_small: int
    padding_medium: int
    padding_large: int

class ButtonStyle(Protocol):
    font: tuple[str, int, str]
    bg: str
    fg: str
    relief: str
    cursor: str
    padx: int
    pady: int

class FrameStyle(Protocol):
    bg: str
    relief: str
    bd: int

class LabelStyle(Protocol):
    font: tuple[str, int]
    bg: str
    fg: str

class ButtonConfig(TypedDict, total=False):
    text: str
    tooltip: str
    shortcut: str