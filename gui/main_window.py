""" This module contains the main window for the image watermarking application. """

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from typing import Optional
import logging
import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from gui import config
from gui import components
from core.application import WatermarkApplication

logger = logging.getLogger(__name__)


class MainWindow(tk.Tk):
    """Main application window with complete functionality."""
    
    def __init__(self, app_controller: WatermarkApplication):
        super().__init__()
        self._app = app_controller
        self._photo_image: Optional[ImageTk.PhotoImage] = None
        
        self.title("Image Watermarking Application")
        self.geometry(f"{config.DIMENSIONS['window_width']}x{config.DIMENSIONS['window_height']}")
        self.minsize(800, 600)  # Minimum size
        self.configure(bg=config.COLORS['background'])
        
        # Variables for UI controls
        self.watermark_text = tk.StringVar(value="© Your Watermark")
        self.font_size = tk.IntVar(value=64)  # Bigger default font
        self.position_x = tk.IntVar(value=85)  # Bottom right position
        self.position_y = tk.IntVar(value=90)  # Bottom right position
        
        # Color controls
        self.watermark_color = tk.StringVar(value="black")  # Default to black
        self.watermark_opacity = tk.IntVar(value=180)  # More opaque (70%)
        
        self._setup_ui()
        self._setup_bindings()
        self._update_ui_state()
        
        logger.info("MainWindow initialized")
    
    def _setup_ui(self):
        """Setup the user interface."""
        self._create_menu()
        self._create_toolbar()
        self._create_main_content()
        self._create_status_bar()
    
    def _create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=self._open_image, accelerator="Ctrl+O")
        file_menu.add_command(label="Save Image", command=self._save_image, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit, accelerator="Ctrl+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Reset Image", command=self._reset_image, accelerator="Ctrl+R")
        edit_menu.add_command(label="Apply Watermark", command=self._apply_watermark, accelerator="Ctrl+W")
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _create_toolbar(self):
        """Create toolbar with buttons."""
        toolbar = tk.Frame(self, bg=config.COLORS['surface'], relief=tk.RAISED, bd=1)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(5, 0))
        
        # File operations group
        file_group = tk.Frame(toolbar, bg=config.COLORS['surface'])
        file_group.pack(side=tk.LEFT, padx=5, pady=5)
        
        components.StyledButton(
            file_group, 
            text="📁 Open Image",
            command=self._open_image
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        components.StyledButton(
            file_group, 
            text="💾 Save Image",
            command=self._save_image
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        # Separator
        separator = tk.Frame(toolbar, width=2, bg=config.COLORS['text_secondary'])
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Watermark operations group
        watermark_group = tk.Frame(toolbar, bg=config.COLORS['surface'])
        watermark_group.pack(side=tk.LEFT, padx=5, pady=5)
        
        components.StyledButton(
            watermark_group, 
            text="🏷️ Apply Watermark",
            command=self._apply_watermark
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        components.StyledButton(
            watermark_group, 
            text="🔄 Reset Image",
            command=self._reset_image
        ).pack(side=tk.LEFT)
        
        # Status info on right side
        status_group = tk.Frame(toolbar, bg=config.COLORS['surface'])
        status_group.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.toolbar_status = tk.Label(
            status_group,
            text="Ready",
            bg=config.COLORS['surface'],
            fg=config.COLORS['text_secondary'],
            font=config.FONTS['small']
        )
        self.toolbar_status.pack(side=tk.RIGHT)
    
    def _create_main_content(self):
        """Create main content area."""
        main_frame = tk.Frame(self, bg=config.COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for image preview
        self._create_image_panel(main_frame)
        
        # Right panel for controls
        self._create_control_panel(main_frame)
    
    def _create_image_panel(self, parent):
        """Create image preview panel."""
        image_frame = tk.LabelFrame(
            parent, 
            text="Image Preview",
            bg=config.COLORS['surface'],
            font=config.FONTS['header']
        )
        image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Image display area
        self.image_label = tk.Label(
            image_frame,
            text="No image loaded\n\nClick 'Open' to load an image",
            bg=config.COLORS['surface'],
            font=config.FONTS['body'],
            compound=tk.CENTER
        )
        self.image_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Image info frame
        info_frame = tk.Frame(image_frame, bg=config.COLORS['surface'])
        info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        self.image_info_label = components.StyledLabel(
            info_frame,
            text="No image information available"
        )
        self.image_info_label.pack(side=tk.LEFT)
    
    def _create_control_panel(self, parent):
        """Create control panel with scrollable content."""
        # Main control frame
        control_frame = tk.LabelFrame(
            parent,
            text="Watermark Settings",
            bg=config.COLORS['surface'],
            font=config.FONTS['header'],
            width=380  # Slightly wider
        )
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        control_frame.pack_propagate(False)
        
        # Create scrollable frame
        canvas = tk.Canvas(control_frame, bg=config.COLORS['surface'], highlightthickness=0)
        scrollbar = tk.Scrollbar(control_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=config.COLORS['surface'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        scrollbar.pack(side="right", fill="y", pady=8)
        
        # Watermark text section (more compact)
        text_frame = tk.LabelFrame(
            scrollable_frame,
            text="Text Settings",
            bg=config.COLORS['surface'],
            font=config.FONTS['body']
        )
        text_frame.pack(fill=tk.X, padx=5, pady=5)
        
        components.StyledLabel(
            text_frame,
            text="Watermark Text:"
        ).pack(anchor=tk.W, padx=5, pady=(5, 2))
        
        components.StyledInput(
            text_frame,
            textvariable=self.watermark_text
        ).pack(fill=tk.X, padx=5, pady=(0, 3))
        
        # Preset buttons (more compact)
        preset_frame = tk.Frame(text_frame, bg=config.COLORS['surface'])
        preset_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        presets = [
            "© Your Name",
            "© 2025",
            "CONFIDENTIAL",
            "SAMPLE",
            "DRAFT"
        ]
        
        for i, preset in enumerate(presets):
            btn = tk.Button(
                preset_frame,
                text=preset,
                font=('Arial', 7),
                command=lambda p=preset: self.watermark_text.set(p),
                bg=config.COLORS['secondary'],
                fg='white',
                relief='flat',
                cursor='hand2'
            )
            btn.grid(row=i//3, column=i%3, sticky='ew', padx=1, pady=1)
        
        for i in range(3):
            preset_frame.columnconfigure(i, weight=1)
        
        # Font test preview button
        test_btn = tk.Button(
            text_frame,
            text="Test Font Size",
            command=self.test_font_size,
            bg=config.COLORS['accent'],
            fg='white',
            font=config.BUTTON_FONT,
            relief='flat'
        )
        test_btn.pack(pady=3, padx=5, fill=tk.X)

        # Font size (compact)
        components.StyledLabel(
            text_frame,
            text="Font Size:"
        ).pack(anchor=tk.W, padx=5, pady=(0, 2))
        
        font_frame = tk.Frame(text_frame, bg=config.COLORS['surface'])
        font_frame.pack(fill=tk.X, padx=5, pady=(0, 3))
        
        # Font size presets
        font_presets = tk.Frame(font_frame, bg=config.COLORS['surface'])
        font_presets.pack(fill=tk.X, pady=(0, 3))
        
        preset_sizes = [24, 48, 64, 96, 128]
        for size in preset_sizes:
            btn = tk.Button(
                font_presets,
                text=f"{size}",
                font=('Arial', 7),
                command=lambda s=size: self.font_size.set(s),
                bg=config.COLORS['secondary'],
                fg='white',
                relief='flat',
                width=4
            )
            btn.pack(side=tk.LEFT, padx=1, fill=tk.X, expand=True)
        
        # Font size slider
        font_control = tk.Frame(font_frame, bg=config.COLORS['surface'])
        font_control.pack(fill=tk.X)
        
        tk.Scale(
            font_control,
            from_=12, to=200,
            orient=tk.HORIZONTAL,
            variable=self.font_size,
            bg=config.COLORS['surface']
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            font_control,
            textvariable=self.font_size,
            bg=config.COLORS['surface'],
            width=4
        ).pack(side=tk.RIGHT)
        
        # Watermark color (more compact)
        components.StyledLabel(
            text_frame,
            text="Color:"
        ).pack(anchor=tk.W, padx=5, pady=(0, 2))
        
        color_frame = tk.Frame(text_frame, bg=config.COLORS['surface'])
        color_frame.pack(fill=tk.X, padx=5, pady=(0, 3))
        
        color_options = [
            ("Black", "black"),
            ("White", "white"),
            ("Red", "red"),
            ("Blue", "blue"),
            ("Yellow", "yellow"),
            ("Green", "green")
        ]
        
        for i, (text, value) in enumerate(color_options):
            tk.Radiobutton(
                color_frame,
                text=text,
                variable=self.watermark_color,
                value=value,
                bg=config.COLORS['surface'],
                font=('Arial', 8)
            ).grid(row=i//3, column=i%3, sticky='w', padx=2)
        
        # Opacity control (compact)
        components.StyledLabel(
            text_frame,
            text="Opacity:"
        ).pack(anchor=tk.W, padx=5, pady=(3, 2))
        
        opacity_frame = tk.Frame(text_frame, bg=config.COLORS['surface'])
        opacity_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        tk.Scale(
            opacity_frame,
            from_=50, to=255,
            orient=tk.HORIZONTAL,
            variable=self.watermark_opacity,
            bg=config.COLORS['surface']
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            opacity_frame,
            textvariable=self.watermark_opacity,
            bg=config.COLORS['surface'],
            width=3
        ).pack(side=tk.RIGHT)
        
        # Position section (more compact)
        pos_frame = tk.LabelFrame(
            scrollable_frame,
            text="Position",
            bg=config.COLORS['surface'],
            font=config.FONTS['body']
        )
        pos_frame.pack(fill=tk.X, padx=5, pady=3)
        
        # X and Y position in one row
        xy_frame = tk.Frame(pos_frame, bg=config.COLORS['surface'])
        xy_frame.pack(fill=tk.X, padx=5, pady=3)
        
        # X Position (left half)
        x_container = tk.Frame(xy_frame, bg=config.COLORS['surface'])
        x_container.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3))
        
        tk.Label(
            x_container,
            text="X:",
            bg=config.COLORS['surface'],
            font=('Arial', 9)
        ).pack(side=tk.TOP, anchor=tk.W)
        
        x_control = tk.Frame(x_container, bg=config.COLORS['surface'])
        x_control.pack(fill=tk.X)
        
        tk.Scale(
            x_control,
            from_=0, to=100,
            orient=tk.HORIZONTAL,
            variable=self.position_x,
            bg=config.COLORS['surface'],
            length=120
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            x_control,
            textvariable=self.position_x,
            bg=config.COLORS['surface'],
            width=3,
            font=('Arial', 8)
        ).pack(side=tk.RIGHT)
        
        # Y Position (right half)
        y_container = tk.Frame(xy_frame, bg=config.COLORS['surface'])
        y_container.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(3, 0))
        
        tk.Label(
            y_container,
            text="Y:",
            bg=config.COLORS['surface'],
            font=('Arial', 9)
        ).pack(side=tk.TOP, anchor=tk.W)
        
        y_control = tk.Frame(y_container, bg=config.COLORS['surface'])
        y_control.pack(fill=tk.X)
        
        tk.Scale(
            y_control,
            from_=0, to=100,
            orient=tk.HORIZONTAL,
            variable=self.position_y,
            bg=config.COLORS['surface'],
            length=120
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            y_control,
            textvariable=self.position_y,
            bg=config.COLORS['surface'],
            width=3,
            font=('Arial', 8)
        ).pack(side=tk.RIGHT)
        
        # Quick position buttons (compact)
        quick_pos_frame = tk.Frame(pos_frame, bg=config.COLORS['surface'])
        quick_pos_frame.pack(fill=tk.X, padx=5, pady=(3, 5))
        
        positions = [
            ("TL", 5, 5),      # Top-Left
            ("TR", 85, 5),     # Top-Right  
            ("C", 45, 45),     # Center
            ("BL", 5, 90),     # Bottom-Left
            ("BR", 85, 90)     # Bottom-Right
        ]
        
        for i, (name, x, y) in enumerate(positions):
            btn = tk.Button(
                quick_pos_frame,
                text=name,
                font=('Arial', 7),
                command=lambda x=x, y=y: self._set_position(x, y),
                bg=config.COLORS['accent'],
                fg='white',
                relief='flat',
                width=4
            )
            btn.grid(row=0, column=i, sticky='ew', padx=1, pady=1)
        
        for i in range(5):
            quick_pos_frame.columnconfigure(i, weight=1)
        
        # Action buttons (at bottom)
        action_frame = tk.Frame(scrollable_frame, bg=config.COLORS['surface'])
        action_frame.pack(fill=tk.X, padx=5, pady=5)
        
        components.StyledButton(
            action_frame,
            text="Apply Watermark",
            command=self._apply_watermark
        ).pack(fill=tk.X, pady=2)
        
        components.StyledButton(
            action_frame,
            text="Reset to Original",
            command=self._reset_image
        ).pack(fill=tk.X, pady=2)
        
        # Bind mousewheel to canvas for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
    
    def _create_status_bar(self):
        """Create status bar."""
        self.status_bar = tk.Label(
            self,
            text="Ready - Load an image to get started",
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg=config.COLORS['surface'],
            font=config.FONTS['small']
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _setup_bindings(self):
        """Setup keyboard bindings."""
        self.bind('<Control-o>', lambda e: self._open_image())
        self.bind('<Control-s>', lambda e: self._save_image())
        self.bind('<Control-r>', lambda e: self._reset_image())
        self.bind('<Control-w>', lambda e: self._apply_watermark())
        self.bind('<Control-q>', lambda e: self.quit())
    
    def _set_position(self, x_percent: int, y_percent: int):
        """Set position using percentage values."""
        self.position_x.set(x_percent)
        self.position_y.set(y_percent)
    
    def _open_image(self):
        """Open image file."""
        try:
            if self._app.load_image_from_dialog():
                self._update_image_display()
                self._update_image_info()
                self._update_status("Image loaded successfully")
                self._update_ui_state()
            else:
                self._update_status("Image loading cancelled")
        except Exception as e:
            logger.error(f"Error opening image: {e}")
            messagebox.showerror("Error", f"Failed to open image: {str(e)}")
            self._update_status("Error loading image")
    
    def _save_image(self):
        """Save current image."""
        if not self._app.has_image:
            messagebox.showwarning("Warning", "No image to save")
            return
        
        try:
            if self._app.save_image_with_dialog():
                self._update_status("Image saved successfully")
            else:
                self._update_status("Save cancelled")
        except Exception as e:
            logger.error(f"Error saving image: {e}")
            messagebox.showerror("Error", f"Failed to save image: {str(e)}")
            self._update_status("Error saving image")
    
    def _apply_watermark(self):
        """Apply watermark to image."""
        if not self._app.has_image:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        text = self.watermark_text.get().strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter watermark text")
            return
        
        try:
            # Calculate position based on percentages
            if self._app.current_image:
                width, height = self._app.current_image.size
                x = int((self.position_x.get() / 100.0) * width)
                y = int((self.position_y.get() / 100.0) * height)
                position = (x, y)
                
                # Get color based on selection
                color_name = self.watermark_color.get()
                opacity = self.watermark_opacity.get()
                font_size = self.font_size.get()
                
                # Debug logging
                logger.info(f"Applying watermark with font size: {font_size}, color: {color_name}, opacity: {opacity}")
                
                color_map = {
                    "black": (0, 0, 0, opacity),
                    "white": (255, 255, 255, opacity),
                    "red": (255, 0, 0, opacity),
                    "blue": (0, 0, 255, opacity),
                    "yellow": (255, 255, 0, opacity),
                    "green": (0, 128, 0, opacity)
                }
                
                color = color_map.get(color_name, (0, 0, 0, opacity))
                
                if self._app.apply_text_watermark(
                    text, 
                    position, 
                    font_size,
                    color
                ):
                    self._update_image_display()
                    self._update_status("Watermark applied successfully")
                else:
                    self._update_status("Failed to apply watermark")
        except Exception as e:
            logger.error(f"Error applying watermark: {e}")
            messagebox.showerror("Error", f"Failed to apply watermark: {str(e)}")
            self._update_status("Error applying watermark")

    def test_font_size(self):
        """Test font size by applying a temporary watermark."""
        try:
            if self._app.has_image:
                # Store current text
                original_text = self.text_var.get()
                
                # Set test text with font size info
                test_text = f"Font Size: {self.font_size.get()}px"
                self.text_var.set(test_text)
                
                # Apply test watermark
                success = self._app.apply_watermark(
                    text=test_text,
                    position=(self.x_position.get(), self.y_position.get()),
                    opacity=self.opacity.get(),
                    size=self.font_size.get(),
                    color=self.color_var.get()
                )
                
                if success:
                    self._update_image_display()
                    self._update_status(f"Font size test: {self.font_size.get()}px")
                    
                    # Restore original text after 3 seconds
                    self.root.after(3000, lambda: self.text_var.set(original_text))
                else:
                    self._update_status("Failed to test font size")
            else:
                messagebox.showwarning("No Image", "Please open an image first")
        except Exception as e:
            logger.error(f"Error testing font size: {e}")
            self._update_status(f"Error: {str(e)}")
    
    def _reset_image(self):
        """Reset image to original."""
        if not self._app.has_image:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        try:
            if self._app.reset_to_original():
                self._update_image_display()
                self._update_status("Image reset to original")
            else:
                self._update_status("Failed to reset image")
        except Exception as e:
            logger.error(f"Error resetting image: {e}")
            messagebox.showerror("Error", f"Failed to reset image: {str(e)}")
    
    def _update_image_display(self):
        """Update image display."""
        try:
            preview_size = (
                config.DIMENSIONS['preview_width'], 
                config.DIMENSIONS['preview_height']
            )
            
            preview_image = self._app.get_preview_image(preview_size)
            
            if preview_image:
                self._photo_image = ImageTk.PhotoImage(preview_image)
                self.image_label.configure(image=self._photo_image, text="")
            else:
                self.image_label.configure(image="", text="Failed to display image")
                
        except Exception as e:
            logger.error(f"Error updating image display: {e}")
            self.image_label.configure(image="", text="Error displaying image")
    
    def _update_image_info(self):
        """Update image information display."""
        try:
            info = self._app.get_image_info()
            if info:
                info_text = f"Size: {info['size'][0]}×{info['size'][1]} | Mode: {info['mode']}"
                self.image_info_label.configure(text=info_text)
            else:
                self.image_info_label.configure(text="No image information available")
        except Exception as e:
            logger.error(f"Error updating image info: {e}")
            self.image_info_label.configure(text="Error reading image info")
    
    def _update_ui_state(self):
        """Update UI state based on current application state."""
        # This method can be used to enable/disable buttons based on state
        pass
    
    def _update_status(self, message: str):
        """Update status bar and toolbar status."""
        self.status_bar.configure(text=message)
        if hasattr(self, 'toolbar_status'):
            # Short version for toolbar
            short_message = message[:20] + "..." if len(message) > 20 else message
            self.toolbar_status.configure(text=short_message)
        logger.info(f"Status: {message}")
    
    def _show_about(self):
        """Show about dialog."""
        about_text = """
Image Watermarking Application
Version 1.0

A modern desktop application for adding watermarks to images.

Features:
• Load and preview images
• Add customizable text watermarks
• Adjustable position and font size
• Save watermarked images
• Reset to original image

Built with Python and Tkinter
        """.strip()
        
        messagebox.showinfo("About", about_text)
    
    def run(self):
        """Start the application."""
        logger.info("Starting application")
        self.mainloop()


# Legacy classes for backward compatibility
class WindowProcessing(MainWindow):
    def __init__(self, app_controller: WatermarkApplication, mode='mono'):
        super().__init__(app_controller)
        self.mode = mode
        title = "Mono Watermarking" if mode == 'mono' else "Batch Watermarking"
        self.title(f'Image Watermarking - {title}')


class WindowMonoProcessing(WindowProcessing):
    def __init__(self, app_controller: WatermarkApplication):
        super().__init__(app_controller, mode='mono')


class WindowBatchProcessing(WindowProcessing):
    def __init__(self, app_controller: WatermarkApplication):
        super().__init__(app_controller, mode='batch')


class HomeWindow(MainWindow):
    def __init__(self, app_controller: WatermarkApplication):
        super().__init__(app_controller)
        # This can be extended for a more complex home screen if needed