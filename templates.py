#!/usr/bin/env python3
"""Design Templates for py-magic-canvas

This module provides pre-designed templates for various use cases:
- Business cards
- Social media posts (Instagram, Twitter, Facebook)
- Flyers
- Posters

Each template includes preset dimensions, colors, and layout suggestions.
"""

from typing import Dict, Tuple, List

class DesignTemplate:
    """Base class for design templates"""
    def __init__(self, name: str, width: int, height: int, 
                 bg_colors: Tuple[int, int, int, int], 
                 description: str = ""):
        self.name = name
        self.width = width
        self.height = height
        self.bg_colors = bg_colors
        self.description = description

class TemplateLibrary:
    """Library of pre-designed templates"""
    
    # Business Card Templates
    BUSINESS_CARD_STANDARD = DesignTemplate(
        name="Business Card - Standard",
        width=1050,
        height=600,
        bg_colors=(255, 255, 255, 255),
        description="Standard business card (3.5 x 2 inches at 300 DPI)"
    )
    
    BUSINESS_CARD_MODERN = DesignTemplate(
        name="Business Card - Modern",
        width=1050,
        height=600,
        bg_colors=(30, 30, 40, 255),
        description="Modern dark business card"
    )
    
    # Social Media Templates
    INSTAGRAM_POST = DesignTemplate(
        name="Instagram Post",
        width=1080,
        height=1080,
        bg_colors=(255, 90, 95, 255),
        description="Instagram square post (1:1 ratio)"
    )
    
    INSTAGRAM_STORY = DesignTemplate(
        name="Instagram Story",
        width=1080,
        height=1920,
        bg_colors=(138, 58, 185, 255),
        description="Instagram story format (9:16 ratio)"
    )
    
    TWITTER_POST = DesignTemplate(
        name="Twitter Post",
        width=1200,
        height=675,
        bg_colors=(29, 161, 242, 255),
        description="Twitter post image (16:9 ratio)"
    )
    
    FACEBOOK_POST = DesignTemplate(
        name="Facebook Post",
        width=1200,
        height=630,
        bg_colors=(59, 89, 152, 255),
        description="Facebook shared image"
    )
    
    # Flyer Templates
    FLYER_A4 = DesignTemplate(
        name="Flyer - A4",
        width=2480,
        height=3508,
        bg_colors=(255, 255, 255, 255),
        description="A4 flyer (8.27 x 11.69 inches at 300 DPI)"
    )
    
    FLYER_LETTER = DesignTemplate(
        name="Flyer - US Letter",
        width=2550,
        height=3300,
        bg_colors=(240, 248, 255, 255),
        description="US Letter size (8.5 x 11 inches at 300 DPI)"
    )
    
    FLYER_HALF_PAGE = DesignTemplate(
        name="Flyer - Half Page",
        width=2550,
        height=1650,
        bg_colors=(255, 250, 240, 255),
        description="Half page flyer (8.5 x 5.5 inches at 300 DPI)"
    )
    
    # Poster Templates
    POSTER_SMALL = DesignTemplate(
        name="Poster - Small",
        width=3300,
        height=5100,
        bg_colors=(255, 255, 255, 255),
        description="Small poster (11 x 17 inches at 300 DPI)"
    )
    
    POSTER_MEDIUM = DesignTemplate(
        name="Poster - Medium",
        width=5400,
        height=7200,
        bg_colors=(245, 245, 250, 255),
        description="Medium poster (18 x 24 inches at 300 DPI)"
    )
    
    @classmethod
    def get_all_templates(cls) -> List[DesignTemplate]:
        """Get all available templates"""
        return [
            cls.BUSINESS_CARD_STANDARD,
            cls.BUSINESS_CARD_MODERN,
            cls.INSTAGRAM_POST,
            cls.INSTAGRAM_STORY,
            cls.TWITTER_POST,
            cls.FACEBOOK_POST,
            cls.FLYER_A4,
            cls.FLYER_LETTER,
            cls.FLYER_HALF_PAGE,
            cls.POSTER_SMALL,
            cls.POSTER_MEDIUM,
        ]
    
    @classmethod
    def get_templates_by_category(cls) -> Dict[str, List[DesignTemplate]]:
        """Get templates organized by category"""
        return {
            "Business Cards": [
                cls.BUSINESS_CARD_STANDARD,
                cls.BUSINESS_CARD_MODERN,
            ],
            "Social Media": [
                cls.INSTAGRAM_POST,
                cls.INSTAGRAM_STORY,
                cls.TWITTER_POST,
                cls.FACEBOOK_POST,
            ],
            "Flyers": [
                cls.FLYER_A4,
                cls.FLYER_LETTER,
                cls.FLYER_HALF_PAGE,
            ],
            "Posters": [
                cls.POSTER_SMALL,
                cls.POSTER_MEDIUM,
            ],
        }
    
    @classmethod
    def get_template_by_name(cls, name: str) -> DesignTemplate:
        """Get a specific template by name"""
        for template in cls.get_all_templates():
            if template.name == name:
                return template
        raise ValueError(f"Template '{name}' not found")
