"""
Simple GUI test script.
"""

import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    print("Testing GUI components...")
    
    # Test config
    import gui.config as config
    print("✓ GUI config imported")
    
    # Test components
    import gui.components as components
    print("✓ GUI components imported")
    
    # Test services
    from gui.services import FileDialogService
    print("✓ GUI services imported")
    
    # Test if tkinter is available
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()  # Hide the window
    print("✓ Tkinter is available")
    root.destroy()
    
    print("\n🎉 GUI components test passed!")
    
except Exception as e:
    print(f"\n❌ Error during GUI testing: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)