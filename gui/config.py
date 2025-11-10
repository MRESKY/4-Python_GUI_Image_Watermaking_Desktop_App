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

# Shortcut for button font
BUTTON_FONT = FONTS['button']

DIMENSIONS = {
    'window_width': 1300,  # Slightly wider
    'window_height': 950,  # Taller for better fit
    'preview_width': 450,  # Bigger preview
    'preview_height': 350,
    'button_height': 35,
    'padding_small': 3,    # Reduced padding
    'padding_medium': 8,
    'padding_large': 15
}

BUTTON_STYLE = {
    'font': FONTS['button'],
    'bg': COLORS['accent'],
    'fg': 'white',
    'relief': 'flat',
    'cursor': 'hand2'
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

INPUT_STYLE = {
    'font': FONTS['body'],
    'bg': COLORS['background'],
    'fg': COLORS['text'],
    'relief': 'solid',
    'bd': 1
}

BUTTONS = {
    "add_single_watermark": {
        "text": "Add Single Image",
    },
    "add_batch_watermark": {
        "text": "Add Batch Images",
    },
    "quit": {
        "text": "Quit",
        "shortcut": "Ctrl+Q"
    },
    "open_image": {
        "text": "Open Image",
        "tooltip": "Open an image to add a watermark",
        "shortcut": "Ctrl+O"
    },
    "save_image": {
        "text": "Save Image",
        "tooltip": "Save the watermarked image",
        "shortcut": "Ctrl+S"
    },
    "apply_watermark": {
        "text": "Apply Watermark",
        "tooltip": "Apply the watermark to the image",
        "shortcut": "Ctrl+A"
    },
    "remove_watermark": {
        "text": "Remove Watermark",
        "tooltip": "Remove the watermark from the image",
        "shortcut": "Ctrl+R"
    },
    "info": {
        "text": "Info",
        "tooltip": "Show application information",
        "shortcut": "F1"
    }
}