#!/usr/bin/env python3
"""Color Palette Management for py-magic-canvas

This module provides:
- Pre-defined color palettes (Material Design, Flat UI, etc.)
- Color harmony generators
- Custom palette creation and management
- Color manipulation utilities
"""

from typing import List, Tuple, Dict
import colorsys
import random

class ColorPalette:
    """Represents a color palette"""
    
    def __init__(self, name: str, colors: List[Tuple[int, int, int]]):
        self.name = name
        self.colors = colors
    
    def get_color(self, index: int) -> Tuple[int, int, int]:
        """Get a color by index (wraps around if index > length)"""
        return self.colors[index % len(self.colors)]
    
    def add_color(self, color: Tuple[int, int, int]):
        """Add a color to the palette"""
        self.colors.append(color)
    
    def remove_color(self, index: int):
        """Remove a color by index"""
        if 0 <= index < len(self.colors):
            del self.colors[index]

class PaletteLibrary:
    """Pre-defined color palettes"""
    
    # Material Design Colors
    MATERIAL_RED = ColorPalette("Material Red", [
        (244, 67, 54),   # Red 500
        (239, 83, 80),   # Red 400
        (229, 115, 115), # Red 300
        (239, 154, 154), # Red 200
    ])
    
    MATERIAL_BLUE = ColorPalette("Material Blue", [
        (33, 150, 243),  # Blue 500
        (66, 165, 245),  # Blue 400
        (100, 181, 246), # Blue 300
        (144, 202, 249), # Blue 200
    ])
    
    MATERIAL_GREEN = ColorPalette("Material Green", [
        (76, 175, 80),   # Green 500
        (102, 187, 106), # Green 400
        (129, 199, 132), # Green 300
        (165, 214, 167), # Green 200
    ])
    
    # Flat UI Colors
    FLAT_UI = ColorPalette("Flat UI", [
        (52, 152, 219),  # Peter River
        (155, 89, 182),  # Amethyst
        (46, 204, 113),  # Emerald
        (241, 196, 15),  # Sun Flower
        (230, 126, 34),  # Carrot
        (231, 76, 60),   # Alizarin
    ])
    
    # Pastel Colors
    PASTEL = ColorPalette("Pastel", [
        (255, 179, 186), # Pink
        (255, 223, 186), # Peach
        (255, 255, 186), # Yellow
        (186, 255, 201), # Green
        (186, 225, 255), # Blue
        (220, 198, 224), # Purple
    ])
    
    # Dark Theme
    DARK_THEME = ColorPalette("Dark Theme", [
        (30, 30, 30),    # Almost Black
        (45, 45, 48),    # Dark Gray
        (60, 63, 65),    # Medium Gray
        (187, 187, 187), # Light Gray
        (255, 255, 255), # White
    ])
    
    # Vibrant Colors
    VIBRANT = ColorPalette("Vibrant", [
        (255, 0, 127),   # Hot Pink
        (0, 255, 255),   # Cyan
        (255, 255, 0),   # Yellow
        (255, 0, 255),   # Magenta
        (0, 255, 0),     # Lime
    ])
    
    # Earth Tones
    EARTH_TONES = ColorPalette("Earth Tones", [
        (139, 90, 43),   # Brown
        (101, 67, 33),   # Dark Brown
        (160, 82, 45),   # Sienna
        (188, 143, 143), # Rosy Brown
        (210, 180, 140), # Tan
    ])
    
    # Ocean Colors
    OCEAN = ColorPalette("Ocean", [
        (0, 105, 148),   # Deep Sea Blue
        (0, 119, 182),   # Ocean Blue
        (3, 169, 244),   # Sky Blue
        (0, 188, 212),   # Cyan
        (77, 208, 225),  # Light Cyan
    ])
    
    # Sunset Colors
    SUNSET = ColorPalette("Sunset", [
        (255, 87, 34),   # Deep Orange
        (255, 112, 67),  # Coral
        (255, 152, 0),   # Orange
        (255, 193, 7),   # Amber
        (255, 235, 59),  # Yellow
    ])
    
    @classmethod
    def get_all_palettes(cls) -> List[ColorPalette]:
        """Get all pre-defined palettes"""
        return [
            cls.MATERIAL_RED,
            cls.MATERIAL_BLUE,
            cls.MATERIAL_GREEN,
            cls.FLAT_UI,
            cls.PASTEL,
            cls.DARK_THEME,
            cls.VIBRANT,
            cls.EARTH_TONES,
            cls.OCEAN,
            cls.SUNSET,
        ]
    
    @classmethod
    def get_palette_by_name(cls, name: str) -> ColorPalette:
        """Get a palette by name"""
        for palette in cls.get_all_palettes():
            if palette.name.lower() == name.lower():
                return palette
        raise ValueError(f"Palette '{name}' not found")

class ColorHarmony:
    """Generate color harmonies from a base color"""
    
    @staticmethod
    def rgb_to_hsv(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
        """Convert RGB to HSV"""
        r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0
        return colorsys.rgb_to_hsv(r, g, b)
    
    @staticmethod
    def hsv_to_rgb(hsv: Tuple[float, float, float]) -> Tuple[int, int, int]:
        """Convert HSV to RGB"""
        r, g, b = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
        return (int(r * 255), int(g * 255), int(b * 255))
    
    @classmethod
    def complementary(cls, base_color: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
        """Generate complementary color harmony"""
        h, s, v = cls.rgb_to_hsv(base_color)
        complement_h = (h + 0.5) % 1.0
        return [
            base_color,
            cls.hsv_to_rgb((complement_h, s, v))
        ]
    
    @classmethod
    def analogous(cls, base_color: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
        """Generate analogous color harmony"""
        h, s, v = cls.rgb_to_hsv(base_color)
        return [
            cls.hsv_to_rgb(((h - 0.083) % 1.0, s, v)),  # -30 degrees
            base_color,
            cls.hsv_to_rgb(((h + 0.083) % 1.0, s, v)),  # +30 degrees
        ]
    
    @classmethod
    def triadic(cls, base_color: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
        """Generate triadic color harmony"""
        h, s, v = cls.rgb_to_hsv(base_color)
        return [
            base_color,
            cls.hsv_to_rgb(((h + 0.333) % 1.0, s, v)),  # +120 degrees
            cls.hsv_to_rgb(((h + 0.666) % 1.0, s, v)),  # +240 degrees
        ]
    
    @classmethod
    def tetradic(cls, base_color: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
        """Generate tetradic (square) color harmony"""
        h, s, v = cls.rgb_to_hsv(base_color)
        return [
            base_color,
            cls.hsv_to_rgb(((h + 0.25) % 1.0, s, v)),   # +90 degrees
            cls.hsv_to_rgb(((h + 0.50) % 1.0, s, v)),   # +180 degrees
            cls.hsv_to_rgb(((h + 0.75) % 1.0, s, v)),   # +270 degrees
        ]
    
    @classmethod
    def monochromatic(cls, base_color: Tuple[int, int, int], count: int = 5) -> List[Tuple[int, int, int]]:
        """Generate monochromatic color harmony"""
        h, s, v = cls.rgb_to_hsv(base_color)
        colors = []
        for i in range(count):
            # Vary the value (brightness)
            new_v = 0.3 + (0.7 * i / (count - 1)) if count > 1 else v
            colors.append(cls.hsv_to_rgb((h, s, new_v)))
        return colors

class ColorUtils:
    """Color manipulation utilities"""
    
    @staticmethod
    def lighten(color: Tuple[int, int, int], amount: float = 0.2) -> Tuple[int, int, int]:
        """Lighten a color by a percentage (0.0-1.0)"""
        return tuple(min(255, int(c + (255 - c) * amount)) for c in color)
    
    @staticmethod
    def darken(color: Tuple[int, int, int], amount: float = 0.2) -> Tuple[int, int, int]:
        """Darken a color by a percentage (0.0-1.0)"""
        return tuple(max(0, int(c * (1 - amount))) for c in color)
    
    @staticmethod
    def blend(color1: Tuple[int, int, int], color2: Tuple[int, int, int], 
             ratio: float = 0.5) -> Tuple[int, int, int]:
        """Blend two colors (ratio: 0.0 = color1, 1.0 = color2)"""
        return tuple(int(c1 * (1 - ratio) + c2 * ratio) 
                    for c1, c2 in zip(color1, color2))
    
    @staticmethod
    def random_color() -> Tuple[int, int, int]:
        """Generate a random color"""
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        """Convert RGB to hex color"""
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
