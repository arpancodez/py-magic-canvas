# py-magic-canvas 🎨✨

**A Python tool for generating custom Canva-style design templates using Tkinter and PIL**

Create stunning posters, banners, and cards with an intuitive GUI interface. Perfect for intermediate Python developers looking to build practical design tools!

## 📋 Overview

Py-Magic-Canvas is a desktop application that empowers users to create professional-looking design templates without the need for expensive design software. Built with Python's Tkinter for the frontend and PIL (Pillow) for high-quality image rendering, this tool demonstrates the power of Python for creative applications.

## ✨ Features

### 🎯 Template Selection
- **Banner Design Mode**: Create eye-catching banners with curved text layouts
- **Semi-circular Text Arrangement**: Text characters are intelligently positioned along an arc
- **Customizable Canvas**: 800x400px canvas optimized for banner designs

### 👁️ Live Preview
- **Real-time Updates**: See your changes instantly in the preview window
- **Interactive Sliders**: Adjust font size dynamically with live feedback
- **Instant Rendering**: No need to wait - changes appear immediately

### 🎨 Text & Image Elements
- **Custom Text Input**: Add any text you want to your banner
- **Font Size Control**: Adjust from 20pt to 80pt for perfect sizing
- **Color Customization**: Set both text and background colors using hex codes
- **Mathematical Text Placement**: Uses trigonometry for precise arc positioning
- **Decorative Elements**: Automatic border and corner accents

### 💾 Export Capabilities
- **PNG Export**: Save your designs as high-quality PNG images
- **JPEG Support**: Alternative format for compatibility
- **File Dialog**: Easy-to-use save interface
- **Multiple Format Options**: Choose the format that works best for you

## 🚀 Getting Started

### Prerequisites

```bash
pip install pillow
```

*Note: Tkinter comes pre-installed with most Python distributions*

### Installation

1. Clone the repository:
```bash
git clone https://github.com/arpancodez/py-magic-canvas.git
cd py-magic-canvas
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## 🎮 Usage

1. **Launch the Application**: Run `python main.py`
2. **Enter Your Text**: Type your banner text in the "Banner Text" field
3. **Adjust Font Size**: Use the slider to find the perfect size
4. **Customize Colors**: Enter hex color codes (e.g., #FF6B6B for red)
5. **Update Preview**: Click "Update Preview" to see your changes
6. **Export**: Click "Export as PNG" when satisfied with your design

## 🛠️ Technical Details

### Architecture
- **GUI Framework**: Tkinter (Python's standard GUI library)
- **Image Processing**: PIL/Pillow for high-quality rendering
- **Mathematical Foundation**: Uses trigonometry for arc text positioning
- **Design Pattern**: Object-oriented with clear separation of concerns

### Key Components
- `MagicCanvasApp`: Main application class
- `_generate_preview()`: Core rendering engine using PIL
- `_add_decorative_elements()`: Adds visual enhancements
- `_export_image()`: Handles file saving operations

## 📝 Code Highlights

The application demonstrates several intermediate Python concepts:
- **Object-Oriented Programming**: Clean class structure
- **GUI Development**: Tkinter widgets and layout management
- **Image Processing**: PIL drawing operations
- **Mathematical Operations**: Trigonometric calculations for text positioning
- **Error Handling**: Try-except blocks for robustness
- **File I/O**: Dialog-based file operations

## 🎨 Example Output

The default banner displays "MAGIC CANVAS" in a beautiful semi-circular arc with:
- Teal background (#4ECDC4)
- Red text (#FF6B6B)
- Decorative border and corner accents
- Professional, polished appearance

## 🔮 Future Enhancements

- [ ] Multiple template types (posters, cards, social media graphics)
- [ ] Image insertion and manipulation
- [ ] Gradient backgrounds
- [ ] Multiple text layers
- [ ] Preset color schemes
- [ ] Shape and icon library
- [ ] Undo/redo functionality
- [ ] Template saving and loading

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- Built with Python's excellent Tkinter library
- Image processing powered by PIL/Pillow
- Inspired by modern design tools like Canva

## 📧 Contact

Created by [@arpancodez](https://github.com/arpancodez)

---

**Happy Designing! 🎨✨**
