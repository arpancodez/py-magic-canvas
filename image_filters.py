#!/usr/bin/env python3
"""Image Filters and Effects for py-magic-canvas

This module provides:
- Built-in PIL filters (blur, sharpen, smooth, etc.)
- Custom filter implementations
- Image adjustment effects (brightness, contrast, saturation)
- Artistic effects
"""

from PIL import Image, ImageFilter, ImageEnhance
from typing import Tuple, Optional
import math

class BasicFilters:
    """Basic image filters using PIL"""
    
    @staticmethod
    def blur(image: Image.Image, radius: int = 2) -> Image.Image:
        """Apply Gaussian blur"""
        return image.filter(ImageFilter.GaussianBlur(radius=radius))
    
    @staticmethod
    def sharpen(image: Image.Image) -> Image.Image:
        """Sharpen the image"""
        return image.filter(ImageFilter.SHARPEN)
    
    @staticmethod
    def smooth(image: Image.Image) -> Image.Image:
        """Smooth the image"""
        return image.filter(ImageFilter.SMOOTH)
    
    @staticmethod
    def edge_enhance(image: Image.Image) -> Image.Image:
        """Enhance edges"""
        return image.filter(ImageFilter.EDGE_ENHANCE)
    
    @staticmethod
    def find_edges(image: Image.Image) -> Image.Image:
        """Find edges in the image"""
        return image.filter(ImageFilter.FIND_EDGES)
    
    @staticmethod
    def emboss(image: Image.Image) -> Image.Image:
        """Apply emboss effect"""
        return image.filter(ImageFilter.EMBOSS)
    
    @staticmethod
    def contour(image: Image.Image) -> Image.Image:
        """Find contours"""
        return image.filter(ImageFilter.CONTOUR)
    
    @staticmethod
    def detail(image: Image.Image) -> Image.Image:
        """Enhance detail"""
        return image.filter(ImageFilter.DETAIL)

class ImageAdjustments:
    """Image adjustment effects"""
    
    @staticmethod
    def brightness(image: Image.Image, factor: float = 1.0) -> Image.Image:
        """Adjust brightness (0.0 = black, 1.0 = original, > 1.0 = brighter)"""
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def contrast(image: Image.Image, factor: float = 1.0) -> Image.Image:
        """Adjust contrast (0.0 = gray, 1.0 = original, > 1.0 = more contrast)"""
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def color(image: Image.Image, factor: float = 1.0) -> Image.Image:
        """Adjust color saturation (0.0 = grayscale, 1.0 = original, > 1.0 = more saturated)"""
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def sharpness(image: Image.Image, factor: float = 1.0) -> Image.Image:
        """Adjust sharpness (0.0 = blurred, 1.0 = original, > 1.0 = sharper)"""
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def auto_contrast(image: Image.Image, cutoff: int = 0) -> Image.Image:
        """Apply auto contrast"""
        from PIL import ImageOps
        return ImageOps.autocontrast(image, cutoff=cutoff)
    
    @staticmethod
    def equalize(image: Image.Image) -> Image.Image:
        """Equalize image histogram"""
        from PIL import ImageOps
        return ImageOps.equalize(image)
    
    @staticmethod
    def invert(image: Image.Image) -> Image.Image:
        """Invert image colors"""
        from PIL import ImageOps
        return ImageOps.invert(image.convert('RGB'))
    
    @staticmethod
    def grayscale(image: Image.Image) -> Image.Image:
        """Convert to grayscale"""
        from PIL import ImageOps
        return ImageOps.grayscale(image)
    
    @staticmethod
    def posterize(image: Image.Image, bits: int = 4) -> Image.Image:
        """Posterize image (reduce color depth)"""
        from PIL import ImageOps
        return ImageOps.posterize(image.convert('RGB'), bits)
    
    @staticmethod
    def solarize(image: Image.Image, threshold: int = 128) -> Image.Image:
        """Solarize image (invert pixels above threshold)"""
        from PIL import ImageOps
        return ImageOps.solarize(image.convert('RGB'), threshold)

class ArtisticEffects:
    """Artistic image effects"""
    
    @staticmethod
    def sepia(image: Image.Image) -> Image.Image:
        """Apply sepia tone effect"""
        # Convert to grayscale first
        gray = image.convert('L')
        # Convert back to RGB
        sepia_img = Image.new('RGB', image.size)
        pixels = sepia_img.load()
        gray_pixels = gray.load()
        
        for y in range(image.height):
            for x in range(image.width):
                gray_val = gray_pixels[x, y]
                # Apply sepia tone
                r = min(255, int(gray_val * 1.0))
                g = min(255, int(gray_val * 0.95))
                b = min(255, int(gray_val * 0.82))
                pixels[x, y] = (r, g, b)
        
        return sepia_img
    
    @staticmethod
    def vignette(image: Image.Image, intensity: float = 0.5) -> Image.Image:
        """Apply vignette effect (darkens edges)"""
        # Create a radial gradient mask
        mask = Image.new('L', image.size, 0)
        mask_pixels = mask.load()
        
        center_x, center_y = image.width // 2, image.height // 2
        max_dist = math.sqrt(center_x**2 + center_y**2)
        
        for y in range(image.height):
            for x in range(image.width):
                # Calculate distance from center
                dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                # Calculate vignette value
                vignette_val = 1.0 - (dist / max_dist) * intensity
                mask_pixels[x, y] = int(vignette_val * 255)
        
        # Apply mask to image
        result = image.copy()
        result.putalpha(mask)
        background = Image.new('RGB', image.size, (0, 0, 0))
        background.paste(result, mask=mask)
        
        return background
    
    @staticmethod
    def pixelate(image: Image.Image, pixel_size: int = 10) -> Image.Image:
        """Apply pixelation effect"""
        # Shrink image
        small = image.resize(
            (image.width // pixel_size, image.height // pixel_size),
            Image.Resampling.NEAREST
        )
        # Enlarge back to original size
        return small.resize(image.size, Image.Resampling.NEAREST)
    
    @staticmethod
    def oil_painting(image: Image.Image, size: int = 5) -> Image.Image:
        """Apply oil painting effect (simplified)"""
        # Use median filter as approximation
        return image.filter(ImageFilter.MedianFilter(size=size))
    
    @staticmethod
    def sketch(image: Image.Image) -> Image.Image:
        """Apply sketch/pencil drawing effect"""
        # Convert to grayscale
        gray = image.convert('L')
        # Invert
        from PIL import ImageOps
        inverted = ImageOps.invert(gray)
        # Blur
        blurred = inverted.filter(ImageFilter.GaussianBlur(radius=5))
        # Blend
        result = Image.blend(gray, blurred, alpha=0.5)
        return result
    
    @staticmethod
    def cartoon(image: Image.Image) -> Image.Image:
        """Apply cartoon effect"""
        # Edge detection
        edges = image.filter(ImageFilter.FIND_EDGES)
        # Posterize
        from PIL import ImageOps
        posterized = ImageOps.posterize(image.convert('RGB'), 4)
        # Combine
        return Image.blend(posterized, edges.convert('RGB'), alpha=0.3)

class FilterPresets:
    """Common filter preset combinations"""
    
    @staticmethod
    def vintage(image: Image.Image) -> Image.Image:
        """Apply vintage/retro effect"""
        # Reduce saturation
        img = ImageAdjustments.color(image, 0.7)
        # Add slight sepia
        img = ArtisticEffects.sepia(img)
        # Reduce contrast slightly
        img = ImageAdjustments.contrast(img, 0.9)
        # Add vignette
        img = ArtisticEffects.vignette(img, 0.3)
        return img
    
    @staticmethod
    def dramatic(image: Image.Image) -> Image.Image:
        """Apply dramatic/cinematic effect"""
        # Increase contrast
        img = ImageAdjustments.contrast(image, 1.3)
        # Reduce saturation slightly
        img = ImageAdjustments.color(img, 0.8)
        # Darken slightly
        img = ImageAdjustments.brightness(img, 0.9)
        # Add vignette
        img = ArtisticEffects.vignette(img, 0.4)
        return img
    
    @staticmethod
    def bright_and_airy(image: Image.Image) -> Image.Image:
        """Apply bright and airy effect"""
        # Increase brightness
        img = ImageAdjustments.brightness(image, 1.2)
        # Reduce contrast
        img = ImageAdjustments.contrast(img, 0.9)
        # Increase saturation
        img = ImageAdjustments.color(img, 1.1)
        return img
    
    @staticmethod
    def black_and_white_contrast(image: Image.Image) -> Image.Image:
        """Apply high-contrast black and white"""
        # Convert to grayscale
        img = ImageAdjustments.grayscale(image)
        # Increase contrast
        img = ImageAdjustments.contrast(img, 1.5)
        return img
