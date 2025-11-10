# 🖼️ Image Watermarking Application

A modern desktop application for adding customizable watermarks to images, built with Python and Tkinter using modern software architecture patterns.

## 🚀 Features

### Core Functionality
- **🖼️ Image Loading**: Support for PNG, JPG, JPEG, GIF, BMP, and TIFF formats
- **💧 Text Watermarks**: Add custom text watermarks with full customization
- **🎨 Visual Customization**: 
  - Font size (12-200px) - **Bigger fonts for better visibility!**
  - Color selection (Black, White, Red, Blue, Yellow, Green)
  - Opacity control (50-255) - **Higher values = more visible**
  - Position control (percentage-based)
- **📍 Quick Positioning**: One-click preset positions (corners, center)
- **💾 Save & Export**: High-quality JPEG output
- **🔄 Reset Functionality**: Restore to original image
- **👁️ Real-time Preview**: Live preview with proper scaling

### User Experience
- **⌨️ Keyboard Shortcuts**: 
  - `Ctrl+O`: Open Image
  - `Ctrl+S`: Save Image
  - `Ctrl+W`: Apply Watermark
  - `Ctrl+R`: Reset Image
  - `Ctrl+Q`: Quit Application
- **🎯 Preset Templates**: Quick watermark text presets
- **📊 Status Updates**: Real-time feedback and progress updates
- **🔧 Error Handling**: Graceful error handling with user-friendly messages

## 🛠️ Installation & Setup

### Quick Start
1. **Install Dependencies**:
```bash
pip install Pillow>=10.0.0
```

2. **Run Application**:
```bash
python main_simple.py
```

## 🎮 How to Use

### For Maximum Watermark Visibility:

#### 1. **📂 Open Your Image**
- Click "📁 Open" button or press `Ctrl+O`
- Select your image file

#### 2. **✍️ Create Visible Watermark**
- **Text**: Use presets or type custom text
- **Font Size**: Start with **64px** (much bigger than default!)
- **Color**: 
  - **Black** for light backgrounds
  - **White** for dark backgrounds  
- **Opacity**: Set to **180+** for clear visibility
- **Position**: Use "Bottom-Right" for standard placement

#### 3. **✅ Apply & Save**
- Click "🏷️ Apply Watermark" or press `Ctrl+W`
- Click "💾 Save" or press `Ctrl+S`

### 💡 Pro Tips for Better Watermarks
- **📏 Size Matters**: Bigger fonts (100-150px) work better on large images
- **🎨 High Contrast**: Dark text on light areas, light text on dark areas
- **👁️ Opacity Balance**: 200+ for copyright protection, 120-180 for subtlety
- **📍 Strategic Placement**: Corner placement doesn't obstruct main subject

## 🏗️ Modern Architecture

Built with professional software design patterns:

### 🧩 **Dependency Injection**
- Loose coupling between components
- Easy testing and maintenance
- Protocol-based interfaces

### 📁 **Clean Structure**
```
📦 Project
├── 🔧 core/              # Business Logic
├── 🖥️ gui/               # User Interface  
├── 🚀 main_simple.py     # Entry Point
└── 📋 requirements.txt   # Dependencies
```

---

**🎯 Ready to create professional watermarks with perfect visibility!**
