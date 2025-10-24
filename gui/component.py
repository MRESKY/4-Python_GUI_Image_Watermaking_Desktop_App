''' This module contains reusable GUI components for the image watermarking application. '''

COLORS = {
    'primary': '#2E3440',
    'secondary': '#3B4252', 
    'accent': '#5E81AC',
    'background': '#ECEFF4',
    'surface': '#FFFFFF',
    'text': '#2E3440',
    'text_secondary': '#4C566A',
    'success': '#A3BE8C',
    'warning': '#EBCB8B',
    'error': '#BF616A'
}

FONTS = {
    'title': ('Helvetica', 20, 'bold'),
    'header': ('Helvetica', 16, 'bold'),
    'body': ('Helvetica', 12),
    'small': ('Helvetica', 10),
    'button': ('Helvetica', 12, 'bold'),
}

DIMENSIONS = {
    'window_width': 1200,
    'window_height': 800,
    'preview_width': 400,
    'preview_height': 300,
    'button_height': 35,
    'padding_small': 5,
    'padding_medium': 10,
    'padding_large': 20
}

BUTTON_STYLE = {
    'font': FONTS['button'],
    'bg': COLORS['accent'],
    'fg': 'white',
    'relief': 'flat',
    'cursor': 'hand2',
    'padx': 15,
    'pady': 5
}

FRAME_STYLE = {
    'bg': COLORS['surface'],
    'relief': 'solid',
    'bd': 1
}

LABEL_STYLE = {
    'font': FONTS['body'],
    'bg': COLORS['surface'],
    'fg': COLORS['text']
}