"""
File dialog service implementation.
"""

from tkinter import filedialog
from typing import Optional, List, Tuple
import logging
import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from core.interfaces import FileDialogService as IFileDialogService

logger = logging.getLogger(__name__)


class FileDialogService(IFileDialogService):
    """Service for file dialog operations."""
    
    def __init__(self):
        self.image_file_types = [
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("GIF files", "*.gif"),
            ("BMP files", "*.bmp"),
            ("TIFF files", "*.tiff"),
            ("All files", "*.*")
        ]
    
    def open_file_dialog(self, file_types: List[Tuple[str, str]] = None) -> Optional[str]:
        """Show file open dialog and return selected path."""
        try:
            if file_types is None:
                file_types = self.image_file_types
            
            file_path = filedialog.askopenfilename(
                title="Open Image File",
                filetypes=file_types
            )
            
            if file_path:
                logger.info(f"File selected: {file_path}")
                return file_path
            else:
                logger.info("No file selected")
                return None
                
        except Exception as e:
            logger.error(f"Error opening file dialog: {e}")
            return None
    
    def save_file_dialog(
        self, 
        default_extension: str = ".jpg", 
        file_types: List[Tuple[str, str]] = None
    ) -> Optional[str]:
        """Show file save dialog and return selected path."""
        try:
            if file_types is None:
                file_types = [
                    ("JPEG files", "*.jpg"),
                    ("PNG files", "*.png"),
                    ("All files", "*.*")
                ]
            
            file_path = filedialog.asksaveasfilename(
                title="Save Image As",
                defaultextension=default_extension,
                filetypes=file_types
            )
            
            if file_path:
                logger.info(f"Save path selected: {file_path}")
                return file_path
            else:
                logger.info("No save path selected")
                return None
                
        except Exception as e:
            logger.error(f"Error opening save dialog: {e}")
            return None
    
    def open_folder_dialog(self) -> Optional[str]:
        """Show folder selection dialog and return selected path."""
        try:
            folder_path = filedialog.askdirectory(
                title="Select Folder"
            )
            
            if folder_path:
                logger.info(f"Folder selected: {folder_path}")
                return folder_path
            else:
                logger.info("No folder selected")
                return None
                
        except Exception as e:
            logger.error(f"Error opening folder dialog: {e}")
            return None