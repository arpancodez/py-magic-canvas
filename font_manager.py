#!/usr/bin/env python3
"""Font Management for py-magic-canvas

This module provides:
- Font discovery and loading
- Font family management
- Font style detection
- Common font collections
"""

from PIL import ImageFont
from typing import List, Dict, Optional, Tuple
import os
import platform

class FontInfo:
    """Information about a font"""
    
    def __init__(self, path: str, family: str, style: str = "Regular"):
        self.path = path
        self.family = family
        self.style = style
    
    def load(self, size: int) -> ImageFont.FreeTypeFont:
        """Load the font with specified size"""
        try:
            return ImageFont.truetype(self.path, size)
        except Exception as e:
            print(f"Failed to load font {self.path}: {e}")
            return ImageFont.load_default()
    
    def __repr__(self) -> str:
        return f"FontInfo(family='{self.family}', style='{self.style}')"

class SystemFontLocator:
    """Locate fonts on the system"""
    
    @staticmethod
    def get_font_directories() -> List[str]:
        """Get common font directories based on OS"""
        system = platform.system()
        
        if system == "Windows":
            return [
                r"C:\Windows\Fonts",
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Windows', 'Fonts')
            ]
        elif system == "Darwin":  # macOS
            return [
                "/System/Library/Fonts",
                "/Library/Fonts",
                os.path.expanduser("~/Library/Fonts")
            ]
        else:  # Linux
            return [
                "/usr/share/fonts",
                "/usr/local/share/fonts",
                os.path.expanduser("~/.fonts"),
                os.path.expanduser("~/.local/share/fonts")
            ]
    
    @classmethod
    def scan_fonts(cls) -> List[FontInfo]:
        """Scan system for available fonts"""
        fonts = []
        directories = cls.get_font_directories()
        
        for directory in directories:
            if not os.path.exists(directory):
                continue
            
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.lower().endswith(('.ttf', '.otf')):
                        path = os.path.join(root, file)
                        # Extract family and style from filename
                        name = os.path.splitext(file)[0]
                        # Simple parsing - can be improved
                        parts = name.replace('-', ' ').split()
                        if len(parts) > 1:
                            family = ' '.join(parts[:-1])
                            style = parts[-1]
                        else:
                            family = name
                            style = "Regular"
                        
                        fonts.append(FontInfo(path, family, style))
        
        return fonts

class CommonFonts:
    """Collection of common cross-platform fonts"""
    
    # Serif fonts
    SERIF_FONTS = [
        "Times New Roman",
        "Georgia",
        "Garamond",
        "Palatino",
        "Baskerville",
        "Liberation Serif",
        "DejaVu Serif",
    ]
    
    # Sans-serif fonts
    SANS_SERIF_FONTS = [
        "Arial",
        "Helvetica",
        "Verdana",
        "Tahoma",
        "Trebuchet MS",
        "Segoe UI",
        "Liberation Sans",
        "DejaVu Sans",
        "Roboto",
    ]
    
    # Monospace fonts
    MONOSPACE_FONTS = [
        "Courier New",
        "Consolas",
        "Monaco",
        "Menlo",
        "Liberation Mono",
        "DejaVu Sans Mono",
    ]
    
    # Decorative fonts
    DECORATIVE_FONTS = [
        "Impact",
        "Comic Sans MS",
        "Brush Script MT",
    ]

class FontManager:
    """Manage fonts for the application"""
    
    def __init__(self):
        self.fonts: Dict[str, List[FontInfo]] = {}
        self._default_font_paths = self._get_default_fonts()
    
    def _get_default_fonts(self) -> Dict[str, str]:
        """Get paths to common default fonts"""
        system = platform.system()
        defaults = {}
        
        if system == "Windows":
            base = r"C:\Windows\Fonts"
            defaults = {
                "Arial": os.path.join(base, "arial.ttf"),
                "Times New Roman": os.path.join(base, "times.ttf"),
                "Courier New": os.path.join(base, "cour.ttf"),
                "Verdana": os.path.join(base, "verdana.ttf"),
            }
        elif system == "Darwin":  # macOS
            defaults = {
                "Arial": "/System/Library/Fonts/Supplemental/Arial.ttf",
                "Helvetica": "/System/Library/Fonts/Helvetica.ttc",
                "Times New Roman": "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
                "Courier": "/System/Library/Fonts/Courier.dfont",
            }
        else:  # Linux
            defaults = {
                "Liberation Sans": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                "Liberation Serif": "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
                "DejaVu Sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "DejaVu Serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
            }
        
        # Filter out non-existent paths
        return {k: v for k, v in defaults.items() if os.path.exists(v)}
    
    def load_system_fonts(self) -> None:
        """Load all system fonts"""
        system_fonts = SystemFontLocator.scan_fonts()
        
        for font in system_fonts:
            if font.family not in self.fonts:
                self.fonts[font.family] = []
            self.fonts[font.family].append(font)
    
    def get_font_families(self) -> List[str]:
        """Get list of available font families"""
        return sorted(self.fonts.keys())
    
    def get_font_styles(self, family: str) -> List[str]:
        """Get available styles for a font family"""
        if family in self.fonts:
            return [font.style for font in self.fonts[family]]
        return []
    
    def get_font(self, family: str, style: str = "Regular", size: int = 12) -> ImageFont.FreeTypeFont:
        """Get a font by family, style, and size"""
        if family in self.fonts:
            for font in self.fonts[family]:
                if font.style == style:
                    return font.load(size)
            # If style not found, use first available
            if self.fonts[family]:
                return self.fonts[family][0].load(size)
        
        # Fallback to default font
        return self.load_default_font(size)
    
    def load_default_font(self, size: int = 12) -> ImageFont.FreeTypeFont:
        """Load a default font"""
        # Try to use one of the default fonts
        for font_path in self._default_font_paths.values():
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
        
        # Last resort: use PIL's default font
        return ImageFont.load_default()
    
    def search_fonts(self, query: str) -> List[str]:
        """Search font families by name"""
        query_lower = query.lower()
        return [family for family in self.fonts.keys() if query_lower in family.lower()]
    
    def get_recommended_fonts(self, category: str = "sans-serif") -> List[str]:
        """Get recommended fonts for a category"""
        if category == "serif":
            candidates = CommonFonts.SERIF_FONTS
        elif category == "sans-serif":
            candidates = CommonFonts.SANS_SERIF_FONTS
        elif category == "monospace":
            candidates = CommonFonts.MONOSPACE_FONTS
        elif category == "decorative":
            candidates = CommonFonts.DECORATIVE_FONTS
        else:
            return []
        
        # Return only fonts that are available on the system
        return [font for font in candidates if font in self.fonts]

# Global font manager instance
_font_manager = None

def get_font_manager() -> FontManager:
    """Get the global font manager instance"""
    global _font_manager
    if _font_manager is None:
        _font_manager = FontManager()
    return _font_manager
