# py-magic-canvas Documentation

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Modules](#modules)
5. [Usage Examples](#usage-examples)
6. [API Reference](#api-reference)
7. [Contributing](#contributing)

## Overview

py-magic-canvas is a comprehensive Python-based design tool built with Tkinter and PIL (Pillow). It provides powerful features for creating banners, social media posts, business cards, and other graphic designs.

### Key Features
- **Design Templates**: Pre-configured templates for various platforms and use cases
- **Drawing Tools**: Advanced shapes, gradients, and text effects
- **Export Options**: Multiple format support with quality settings
- **Color Management**: Pre-defined palettes and color harmony generators
- **Undo/Redo**: Full history management with command pattern
- **Image Filters**: Comprehensive filter and effects library
- **Canvas Presets**: Platform-specific canvas sizes
- **Font Management**: System font discovery and loading
- **Enhanced UI**: Custom components and intuitive controls

## Installation

### Requirements
- Python 3.7+
- PIL/Pillow
- Tkinter (usually included with Python)

### Setup
```bash
pip install pillow
```

## Quick Start

```python
import tkinter as tk
from main import BannerDesigner

root = tk.Tk()
app = BannerDesigner(root)
root.mainloop()
```

## Modules

### 1. templates.py
Provides pre-designed templates for various use cases.

**Key Classes:**
- `DesignTemplate`: Base template class
- `TemplateLibrary`: Collection of predefined templates

**Example:**
```python
from templates import TemplateLibrary

# Get Instagram post template
template = TemplateLibrary.INSTAGRAM_POST
print(f"Size: {template.width}x{template.height}")
```

### 2. drawing_tools.py
Advanced drawing capabilities for shapes, gradients, and text effects.

**Key Classes:**
- `ShapeTools`: Draw rectangles, circles, stars, polygons, arrows
- `GradientTools`: Create linear and radial gradients
- `TextEffects`: Apply outline, shadow, and glow effects

**Example:**
```python
from drawing_tools import ShapeTools, GradientTools
from PIL import Image, ImageDraw

img = Image.new('RGB', (800, 600), 'white')
draw = ImageDraw.Draw(img)

# Draw a star
ShapeTools.draw_star(draw, (400, 300), 100, 50, points=5, 
                     fill=(255, 215, 0), outline=(0, 0, 0))

# Create gradient
grad = GradientTools.create_linear_gradient(800, 600, 
                                            (255, 0, 0), (0, 0, 255))
```

### 3. export_options.py
Comprehensive export functionality with multiple formats and quality settings.

**Key Classes:**
- `ExportFormat`: Supported format constants
- `ExportSettings`: Configuration for export options
- `ImageExporter`: Main export functionality

**Example:**
```python
from export_options import ImageExporter, ExportSettings, ExportFormat

settings = ExportSettings()
settings.format = ExportFormat.JPEG
settings.quality = 95
settings.dpi = (300, 300)

ImageExporter.export_image(image, 'output.jpg', settings)
```

### 4. color_palettes.py
Color palette management with harmonies and utilities.

**Key Classes:**
- `ColorPalette`: Palette representation
- `PaletteLibrary`: Pre-defined color palettes
- `ColorHarmony`: Generate color harmonies
- `ColorUtils`: Color manipulation utilities

**Example:**
```python
from color_palettes import PaletteLibrary, ColorHarmony

# Get a palette
palette = PaletteLibrary.MATERIAL_BLUE
print(palette.colors)

# Generate complementary colors
base_color = (255, 0, 0)
colors = ColorHarmony.complementary(base_color)
print(colors)
```

### 5. undo_redo.py
Undo/redo functionality using command pattern.

**Key Classes:**
- `Command`: Abstract command base class
- `HistoryManager`: Manage undo/redo history
- `PropertyChangeCommand`: Command for property changes
- `CompositeCommand`: Group multiple commands

**Example:**
```python
from undo_redo import HistoryManager, PropertyChangeCommand

history = HistoryManager(max_history=50)

# Execute a command
cmd = PropertyChangeCommand(obj, 'property_name', new_value)
history.execute_command(cmd)

# Undo
history.undo()

# Redo
history.redo()
```

### 6. image_filters.py
Image filters and effects library.

**Key Classes:**
- `BasicFilters`: Blur, sharpen, emboss, etc.
- `ImageAdjustments`: Brightness, contrast, saturation
- `ArtisticEffects`: Sepia, vignette, pixelate, sketch
- `FilterPresets`: Common filter combinations

**Example:**
```python
from image_filters import BasicFilters, ArtisticEffects, FilterPresets

# Apply blur
blurred = BasicFilters.blur(image, radius=5)

# Apply sepia effect
sepia = ArtisticEffects.sepia(image)

# Apply vintage preset
vintage = FilterPresets.vintage(image)
```

### 7. canvas_presets.py
Canvas size presets for various platforms.

**Key Classes:**
- `CanvasPreset`: Preset representation
- `SocialMediaPresets`: Instagram, Facebook, Twitter, etc.
- `PrintPresets`: Business cards, posters, flyers
- `DigitalPresets`: Wallpapers, banners
- `PresetManager`: Query and search presets

**Example:**
```python
from canvas_presets import SocialMediaPresets, PresetManager

# Get Instagram story preset
preset = SocialMediaPresets.INSTAGRAM_STORY
print(f"Size: {preset.width}x{preset.height}")

# Search presets
results = PresetManager.search_presets('instagram')
```

### 8. font_manager.py
Font management system.

**Key Classes:**
- `FontInfo`: Font information
- `SystemFontLocator`: Locate system fonts
- `CommonFonts`: Collections of common fonts
- `FontManager`: Manage fonts for the application

**Example:**
```python
from font_manager import get_font_manager

font_mgr = get_font_manager()
font_mgr.load_system_fonts()

# Get available font families
families = font_mgr.get_font_families()

# Load a specific font
font = font_mgr.get_font('Arial', 'Regular', size=24)
```

### 9. ui_components.py
Enhanced UI components for Tkinter.

**Key Classes:**
- `StyledButton`: Custom styled button with hover effects
- `ColorPicker`: Color selection component
- `SliderControl`: Labeled slider
- `ToolPanel`: Tool selection panel
- `PropertyInspector`: Property editing panel
- `Toolbar`: Application toolbar
- `StatusBar`: Status bar component

**Example:**
```python
from ui_components import ColorPicker, SliderControl, Toolbar
import tkinter as tk

root = tk.Tk()

# Add color picker
color_picker = ColorPicker(root, on_change=lambda c: print(c))
color_picker.pack()

# Add slider
slider = SliderControl(root, label='Opacity', from_=0, to=100)
slider.pack()

# Add toolbar
toolbar = Toolbar(root)
toolbar.add_button('New', command=lambda: print('New'))
toolbar.add_separator()
toolbar.add_button('Save', command=lambda: print('Save'))
```

## Usage Examples

### Example 1: Creating a Social Media Post

```python
from PIL import Image, ImageDraw
from canvas_presets import SocialMediaPresets
from color_palettes import PaletteLibrary
from drawing_tools import GradientTools, TextEffects

# Get preset
preset = SocialMediaPresets.INSTAGRAM_POST

# Create image with gradient
grad = GradientTools.create_radial_gradient(
    preset.width, preset.height,
    (138, 58, 185), (252, 176, 69)
)

# Add text with effects
draw = ImageDraw.Draw(grad)
font = ImageFont.truetype('arial.ttf', 60)
TextEffects.draw_text_with_outline(
    draw, (preset.width//2, preset.height//2),
    'Hello World!', font, (255, 255, 255, 255), (0, 0, 0, 255)
)

grad.show()
```

### Example 2: Applying Filters

```python
from PIL import Image
from image_filters import FilterPresets, ImageAdjustments

# Load image
img = Image.open('photo.jpg')

# Apply vintage filter
vintage = FilterPresets.vintage(img)

# Adjust brightness
bright = ImageAdjustments.brightness(vintage, 1.2)

bright.save('output.jpg')
```

### Example 3: Using Undo/Redo

```python
from undo_redo import HistoryManager, CallbackCommand

history = HistoryManager()

state = {'value': 0}

def increment():
    state['value'] += 1
    print(f"Value: {state['value']}")

def decrement():
    state['value'] -= 1
    print(f"Value: {state['value']}")

cmd = CallbackCommand(increment, decrement)
history.execute_command(cmd)  # Value: 1
history.undo()  # Value: 0
history.redo()  # Value: 1
```

## API Reference

For detailed API documentation, refer to the docstrings in each module. All classes and methods include comprehensive documentation.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes with clear commit messages
4. Add tests if applicable
5. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Include docstrings for all public methods
- Keep functions focused and modular

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please visit the GitHub repository.
