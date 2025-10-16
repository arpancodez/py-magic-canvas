#!/usr/bin/env python3
"""Export Options for py-magic-canvas

This module provides advanced export functionality:
- Multiple file format support (PNG, JPEG, WebP, BMP, TIFF, PDF)
- Quality settings for lossy formats
- Resolution/DPI settings
- Compression options
- Batch export capabilities
"""

from PIL import Image
from typing import Dict, List, Tuple, Optional
import os

class ExportFormat:
    """Supported export formats"""
    PNG = 'PNG'
    JPEG = 'JPEG'
    WEBP = 'WebP'
    BMP = 'BMP'
    TIFF = 'TIFF'
    PDF = 'PDF'
    GIF = 'GIF'
    
    @classmethod
    def get_all_formats(cls) -> List[str]:
        """Get all supported formats"""
        return [cls.PNG, cls.JPEG, cls.WEBP, cls.BMP, cls.TIFF, cls.PDF, cls.GIF]
    
    @classmethod
    def get_extensions(cls) -> Dict[str, str]:
        """Get file extensions for each format"""
        return {
            cls.PNG: '.png',
            cls.JPEG: '.jpg',
            cls.WEBP: '.webp',
            cls.BMP: '.bmp',
            cls.TIFF: '.tiff',
            cls.PDF: '.pdf',
            cls.GIF: '.gif',
        }

class ExportSettings:
    """Export settings configuration"""
    
    def __init__(self):
        self.format = ExportFormat.PNG
        self.quality = 95  # For JPEG/WebP (1-100)
        self.dpi = (300, 300)  # DPI for print formats
        self.optimize = True  # Optimize file size
        self.compression = 6  # PNG compression (0-9)
        self.progressive = False  # Progressive JPEG
        
class ImageExporter:
    """Advanced image export functionality"""
    
    @staticmethod
    def export_image(image: Image.Image, 
                    filepath: str,
                    settings: Optional[ExportSettings] = None) -> bool:
        """Export image with specified settings
        
        Args:
            image: PIL Image to export
            filepath: Output file path
            settings: Export settings (uses defaults if None)
            
        Returns:
            True if export succeeded, False otherwise
        """
        if settings is None:
            settings = ExportSettings()
        
        try:
            # Get format from settings or file extension
            fmt = settings.format
            if not fmt:
                ext = os.path.splitext(filepath)[1].lower()
                fmt_map = {v: k for k, v in ExportFormat.get_extensions().items()}
                fmt = fmt_map.get(ext, ExportFormat.PNG)
            
            # Prepare image based on format
            export_img = image
            
            # Convert to RGB for formats that don't support transparency
            if fmt in [ExportFormat.JPEG, ExportFormat.BMP, ExportFormat.PDF]:
                if export_img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background
                    background = Image.new('RGB', export_img.size, (255, 255, 255))
                    if export_img.mode == 'P':
                        export_img = export_img.convert('RGBA')
                    background.paste(export_img, mask=export_img.split()[-1] if export_img.mode in ('RGBA', 'LA') else None)
                    export_img = background
                elif export_img.mode != 'RGB':
                    export_img = export_img.convert('RGB')
            
            # Format-specific export
            save_kwargs = {}
            
            if fmt == ExportFormat.PNG:
                save_kwargs['optimize'] = settings.optimize
                save_kwargs['compress_level'] = settings.compression
                save_kwargs['dpi'] = settings.dpi
                
            elif fmt == ExportFormat.JPEG:
                save_kwargs['quality'] = settings.quality
                save_kwargs['optimize'] = settings.optimize
                save_kwargs['progressive'] = settings.progressive
                save_kwargs['dpi'] = settings.dpi
                
            elif fmt == ExportFormat.WEBP:
                save_kwargs['quality'] = settings.quality
                save_kwargs['method'] = 6  # Compression method (0-6)
                
            elif fmt == ExportFormat.TIFF:
                save_kwargs['compression'] = 'tiff_deflate'
                save_kwargs['dpi'] = settings.dpi
                
            elif fmt == ExportFormat.PDF:
                save_kwargs['resolution'] = settings.dpi[0]
                
            # Save the image
            export_img.save(filepath, format=fmt, **save_kwargs)
            return True
            
        except Exception as e:
            print(f"Export error: {e}")
            return False
    
    @staticmethod
    def batch_export(image: Image.Image,
                    base_path: str,
                    formats: List[str],
                    settings_per_format: Optional[Dict[str, ExportSettings]] = None) -> Dict[str, bool]:
        """Export image in multiple formats
        
        Args:
            image: PIL Image to export
            base_path: Base file path (without extension)
            formats: List of formats to export
            settings_per_format: Optional settings for each format
            
        Returns:
            Dictionary mapping format to success status
        """
        results = {}
        
        for fmt in formats:
            ext = ExportFormat.get_extensions().get(fmt, '.png')
            filepath = f"{base_path}{ext}"
            
            settings = None
            if settings_per_format and fmt in settings_per_format:
                settings = settings_per_format[fmt]
            else:
                settings = ExportSettings()
                settings.format = fmt
            
            success = ImageExporter.export_image(image, filepath, settings)
            results[fmt] = success
        
        return results
    
    @staticmethod
    def create_thumbnail(image: Image.Image,
                        size: Tuple[int, int] = (256, 256),
                        maintain_aspect: bool = True) -> Image.Image:
        """Create a thumbnail of the image
        
        Args:
            image: Source image
            size: Thumbnail size (width, height)
            maintain_aspect: Whether to maintain aspect ratio
            
        Returns:
            Thumbnail image
        """
        thumb = image.copy()
        if maintain_aspect:
            thumb.thumbnail(size, Image.Resampling.LANCZOS)
        else:
            thumb = thumb.resize(size, Image.Resampling.LANCZOS)
        return thumb
    
    @staticmethod
    def get_export_presets() -> Dict[str, ExportSettings]:
        """Get common export presets"""
        presets = {}
        
        # Web optimized
        web = ExportSettings()
        web.format = ExportFormat.JPEG
        web.quality = 85
        web.optimize = True
        web.progressive = True
        presets['web'] = web
        
        # Print quality
        print_preset = ExportSettings()
        print_preset.format = ExportFormat.PNG
        print_preset.dpi = (300, 300)
        print_preset.optimize = False
        presets['print'] = print_preset
        
        # High quality
        high_quality = ExportSettings()
        high_quality.format = ExportFormat.PNG
        high_quality.compression = 3
        high_quality.optimize = False
        presets['high_quality'] = high_quality
        
        # Small file size
        small = ExportSettings()
        small.format = ExportFormat.JPEG
        small.quality = 70
        small.optimize = True
        presets['small_size'] = small
        
        return presets
