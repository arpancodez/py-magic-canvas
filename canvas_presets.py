#!/usr/bin/env python3
"""Canvas Presets for py-magic-canvas

This module provides preset canvas sizes for various platforms and use cases:
- Social media platforms (Instagram, Twitter, Facebook, LinkedIn, etc.)
- Print formats (business cards, posters, flyers)
- Digital formats (desktop, mobile, web banners)
- Video formats (YouTube, TikTok, etc.)
"""

from typing import Tuple, Dict, List
from dataclasses import dataclass

@dataclass
class CanvasPreset:
    """Represents a canvas size preset"""
    name: str
    width: int
    height: int
    category: str
    description: str = ""
    dpi: int = 72  # Default for digital
    
    @property
    def size(self) -> Tuple[int, int]:
        """Get canvas size as tuple"""
        return (self.width, self.height)
    
    @property
    def aspect_ratio(self) -> float:
        """Get aspect ratio"""
        return self.width / self.height

class SocialMediaPresets:
    """Social media canvas presets"""
    
    # Instagram
    INSTAGRAM_POST = CanvasPreset(
        "Instagram Post (Square)", 1080, 1080, "Instagram",
        "Square post format (1:1)"
    )
    
    INSTAGRAM_PORTRAIT = CanvasPreset(
        "Instagram Portrait", 1080, 1350, "Instagram",
        "Portrait post format (4:5)"
    )
    
    INSTAGRAM_LANDSCAPE = CanvasPreset(
        "Instagram Landscape", 1080, 566, "Instagram",
        "Landscape post format (1.91:1)"
    )
    
    INSTAGRAM_STORY = CanvasPreset(
        "Instagram Story", 1080, 1920, "Instagram",
        "Story format (9:16)"
    )
    
    INSTAGRAM_REEL = CanvasPreset(
        "Instagram Reel", 1080, 1920, "Instagram",
        "Reel format (9:16)"
    )
    
    # Facebook
    FACEBOOK_POST = CanvasPreset(
        "Facebook Post", 1200, 630, "Facebook",
        "Link preview image"
    )
    
    FACEBOOK_COVER = CanvasPreset(
        "Facebook Cover Photo", 820, 312, "Facebook",
        "Profile cover photo"
    )
    
    FACEBOOK_STORY = CanvasPreset(
        "Facebook Story", 1080, 1920, "Facebook",
        "Story format (9:16)"
    )
    
    # Twitter/X
    TWITTER_POST = CanvasPreset(
        "Twitter/X Post", 1200, 675, "Twitter",
        "Post image (16:9)"
    )
    
    TWITTER_HEADER = CanvasPreset(
        "Twitter/X Header", 1500, 500, "Twitter",
        "Profile header image"
    )
    
    # LinkedIn
    LINKEDIN_POST = CanvasPreset(
        "LinkedIn Post", 1200, 627, "LinkedIn",
        "Post image"
    )
    
    LINKEDIN_COVER = CanvasPreset(
        "LinkedIn Cover", 1584, 396, "LinkedIn",
        "Profile background"
    )
    
    # Pinterest
    PINTEREST_PIN = CanvasPreset(
        "Pinterest Pin", 1000, 1500, "Pinterest",
        "Standard pin (2:3)"
    )
    
    # YouTube
    YOUTUBE_THUMBNAIL = CanvasPreset(
        "YouTube Thumbnail", 1280, 720, "YouTube",
        "Video thumbnail (16:9)"
    )
    
    YOUTUBE_CHANNEL_ART = CanvasPreset(
        "YouTube Channel Art", 2560, 1440, "YouTube",
        "Channel banner"
    )
    
    # TikTok
    TIKTOK_VIDEO = CanvasPreset(
        "TikTok Video", 1080, 1920, "TikTok",
        "Video format (9:16)"
    )

class PrintPresets:
    """Print format canvas presets"""
    
    # Business Cards (at 300 DPI)
    BUSINESS_CARD_US = CanvasPreset(
        "Business Card (US)", 1050, 600, "Print",
        "3.5 x 2 inches", dpi=300
    )
    
    BUSINESS_CARD_EU = CanvasPreset(
        "Business Card (EU)", 1063, 638, "Print",
        "85 x 55 mm", dpi=300
    )
    
    # Posters
    POSTER_A4 = CanvasPreset(
        "Poster A4", 2480, 3508, "Print",
        "210 x 297 mm (8.27 x 11.69 inches)", dpi=300
    )
    
    POSTER_A3 = CanvasPreset(
        "Poster A3", 3508, 4961, "Print",
        "297 x 420 mm (11.69 x 16.54 inches)", dpi=300
    )
    
    POSTER_11X17 = CanvasPreset(
        "Poster 11x17\"", 3300, 5100, "Print",
        "11 x 17 inches (Tabloid)", dpi=300
    )
    
    POSTER_18X24 = CanvasPreset(
        "Poster 18x24\"", 5400, 7200, "Print",
        "18 x 24 inches", dpi=300
    )
    
    # Flyers
    FLYER_LETTER = CanvasPreset(
        "Flyer (US Letter)", 2550, 3300, "Print",
        "8.5 x 11 inches", dpi=300
    )
    
    FLYER_A5 = CanvasPreset(
        "Flyer A5", 1748, 2480, "Print",
        "148 x 210 mm (5.83 x 8.27 inches)", dpi=300
    )
    
    # Postcards
    POSTCARD_4X6 = CanvasPreset(
        "Postcard 4x6\"", 1200, 1800, "Print",
        "4 x 6 inches", dpi=300
    )
    
    POSTCARD_5X7 = CanvasPreset(
        "Postcard 5x7\"", 1500, 2100, "Print",
        "5 x 7 inches", dpi=300
    )

class DigitalPresets:
    """Digital/web canvas presets"""
    
    # Desktop Wallpapers
    WALLPAPER_FHD = CanvasPreset(
        "Desktop Wallpaper (FHD)", 1920, 1080, "Digital",
        "Full HD (1920x1080)"
    )
    
    WALLPAPER_QHD = CanvasPreset(
        "Desktop Wallpaper (QHD)", 2560, 1440, "Digital",
        "Quad HD (2560x1440)"
    )
    
    WALLPAPER_4K = CanvasPreset(
        "Desktop Wallpaper (4K)", 3840, 2160, "Digital",
        "4K Ultra HD (3840x2160)"
    )
    
    # Mobile Wallpapers
    MOBILE_WALLPAPER_IPHONE = CanvasPreset(
        "iPhone Wallpaper", 1170, 2532, "Digital",
        "iPhone 14/15 Pro"
    )
    
    MOBILE_WALLPAPER_ANDROID = CanvasPreset(
        "Android Wallpaper", 1440, 3200, "Digital",
        "Common Android resolution"
    )
    
    # Web Banners
    BANNER_LEADERBOARD = CanvasPreset(
        "Leaderboard Banner", 728, 90, "Digital",
        "Standard web banner"
    )
    
    BANNER_LARGE = CanvasPreset(
        "Large Rectangle Banner", 336, 280, "Digital",
        "Large rectangle ad"
    )
    
    BANNER_SKYSCRAPER = CanvasPreset(
        "Skyscraper Banner", 160, 600, "Digital",
        "Wide skyscraper ad"
    )
    
    # Email
    EMAIL_HEADER = CanvasPreset(
        "Email Header", 600, 200, "Digital",
        "Standard email header width"
    )
    
    # Blog/Website
    BLOG_FEATURED = CanvasPreset(
        "Blog Featured Image", 1200, 630, "Digital",
        "Open Graph standard size"
    )

class PresetManager:
    """Manage and query canvas presets"""
    
    @classmethod
    def get_all_presets(cls) -> List[CanvasPreset]:
        """Get all available presets"""
        presets = []
        
        # Social media
        for attr in dir(SocialMediaPresets):
            if not attr.startswith('_'):
                val = getattr(SocialMediaPresets, attr)
                if isinstance(val, CanvasPreset):
                    presets.append(val)
        
        # Print
        for attr in dir(PrintPresets):
            if not attr.startswith('_'):
                val = getattr(PrintPresets, attr)
                if isinstance(val, CanvasPreset):
                    presets.append(val)
        
        # Digital
        for attr in dir(DigitalPresets):
            if not attr.startswith('_'):
                val = getattr(DigitalPresets, attr)
                if isinstance(val, CanvasPreset):
                    presets.append(val)
        
        return presets
    
    @classmethod
    def get_by_category(cls) -> Dict[str, List[CanvasPreset]]:
        """Get presets organized by category"""
        all_presets = cls.get_all_presets()
        categories = {}
        
        for preset in all_presets:
            if preset.category not in categories:
                categories[preset.category] = []
            categories[preset.category].append(preset)
        
        return categories
    
    @classmethod
    def search_presets(cls, keyword: str) -> List[CanvasPreset]:
        """Search presets by keyword"""
        keyword_lower = keyword.lower()
        return [
            preset for preset in cls.get_all_presets()
            if keyword_lower in preset.name.lower() or 
               keyword_lower in preset.description.lower() or
               keyword_lower in preset.category.lower()
        ]
    
    @classmethod
    def get_by_aspect_ratio(cls, aspect_ratio: float, tolerance: float = 0.1) -> List[CanvasPreset]:
        """Get presets matching a specific aspect ratio"""
        return [
            preset for preset in cls.get_all_presets()
            if abs(preset.aspect_ratio - aspect_ratio) <= tolerance
        ]
