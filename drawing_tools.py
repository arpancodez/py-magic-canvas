#!/usr/bin/env python3
"""Drawing Tools for py-magic-canvas

This module provides advanced drawing tools:
- Shape drawing (rectangles, circles, ellipses, polygons, stars)
- Text effects (shadow, outline, gradient text)
- Gradient generators (linear, radial, conic)
- Pattern fills
"""

from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, List, Optional
import math

class ShapeTools:
    """Tools for drawing various shapes"""
    
    @staticmethod
    def draw_rectangle(draw: ImageDraw.ImageDraw, 
                      xy: Tuple[int, int, int, int],
                      fill: Tuple[int, int, int, int] = None,
                      outline: Tuple[int, int, int, int] = None,
                      width: int = 1,
                      rounded: bool = False,
                      radius: int = 0):
        """Draw a rectangle with optional rounded corners"""
        if rounded:
            draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)
        else:
            draw.rectangle(xy, fill=fill, outline=outline, width=width)
    
    @staticmethod
    def draw_circle(draw: ImageDraw.ImageDraw,
                   center: Tuple[int, int],
                   radius: int,
                   fill: Tuple[int, int, int, int] = None,
                   outline: Tuple[int, int, int, int] = None,
                   width: int = 1):
        """Draw a circle"""
        x, y = center
        bbox = [x - radius, y - radius, x + radius, y + radius]
        draw.ellipse(bbox, fill=fill, outline=outline, width=width)
    
    @staticmethod
    def draw_star(draw: ImageDraw.ImageDraw,
                 center: Tuple[int, int],
                 outer_radius: int,
                 inner_radius: int,
                 points: int = 5,
                 fill: Tuple[int, int, int, int] = None,
                 outline: Tuple[int, int, int, int] = None,
                 width: int = 1):
        """Draw a star shape"""
        x, y = center
        coords = []
        for i in range(points * 2):
            angle = math.pi / 2 + (2 * math.pi * i) / (points * 2)
            radius = outer_radius if i % 2 == 0 else inner_radius
            px = x + radius * math.cos(angle)
            py = y - radius * math.sin(angle)
            coords.append((px, py))
        draw.polygon(coords, fill=fill, outline=outline, width=width)
    
    @staticmethod
    def draw_polygon(draw: ImageDraw.ImageDraw,
                    points: List[Tuple[int, int]],
                    fill: Tuple[int, int, int, int] = None,
                    outline: Tuple[int, int, int, int] = None,
                    width: int = 1):
        """Draw a polygon from a list of points"""
        draw.polygon(points, fill=fill, outline=outline, width=width)
    
    @staticmethod
    def draw_arrow(draw: ImageDraw.ImageDraw,
                  start: Tuple[int, int],
                  end: Tuple[int, int],
                  width: int = 5,
                  arrow_size: int = 20,
                  fill: Tuple[int, int, int, int] = (0, 0, 0, 255)):
        """Draw an arrow from start to end point"""
        # Draw main line
        draw.line([start, end], fill=fill, width=width)
        
        # Calculate arrow head
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.sqrt(dx**2 + dy**2)
        if length == 0:
            return
        
        # Unit vector
        ux = dx / length
        uy = dy / length
        
        # Perpendicular vector
        px = -uy
        py = ux
        
        # Arrow head points
        p1 = end
        p2 = (end[0] - arrow_size * ux + arrow_size/2 * px,
              end[1] - arrow_size * uy + arrow_size/2 * py)
        p3 = (end[0] - arrow_size * ux - arrow_size/2 * px,
              end[1] - arrow_size * uy - arrow_size/2 * py)
        
        draw.polygon([p1, p2, p3], fill=fill)

class GradientTools:
    """Tools for creating gradients"""
    
    @staticmethod
    def create_linear_gradient(width: int, height: int,
                             color1: Tuple[int, int, int],
                             color2: Tuple[int, int, int],
                             direction: str = 'horizontal') -> Image.Image:
        """Create a linear gradient
        
        direction: 'horizontal', 'vertical', 'diagonal'
        """
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        if direction == 'horizontal':
            for x in range(width):
                r = int(color1[0] + (color2[0] - color1[0]) * x / width)
                g = int(color1[1] + (color2[1] - color1[1]) * x / width)
                b = int(color1[2] + (color2[2] - color1[2]) * x / width)
                draw.line([(x, 0), (x, height)], fill=(r, g, b))
        
        elif direction == 'vertical':
            for y in range(height):
                r = int(color1[0] + (color2[0] - color1[0]) * y / height)
                g = int(color1[1] + (color2[1] - color1[1]) * y / height)
                b = int(color1[2] + (color2[2] - color1[2]) * y / height)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        elif direction == 'diagonal':
            max_dist = math.sqrt(width**2 + height**2)
            for y in range(height):
                for x in range(width):
                    dist = math.sqrt(x**2 + y**2)
                    t = dist / max_dist
                    r = int(color1[0] + (color2[0] - color1[0]) * t)
                    g = int(color1[1] + (color2[1] - color1[1]) * t)
                    b = int(color1[2] + (color2[2] - color1[2]) * t)
                    img.putpixel((x, y), (r, g, b))
        
        return img
    
    @staticmethod
    def create_radial_gradient(width: int, height: int,
                             color1: Tuple[int, int, int],
                             color2: Tuple[int, int, int],
                             center: Optional[Tuple[int, int]] = None) -> Image.Image:
        """Create a radial gradient"""
        img = Image.new('RGB', (width, height))
        
        if center is None:
            center = (width // 2, height // 2)
        
        max_dist = math.sqrt((width/2)**2 + (height/2)**2)
        
        for y in range(height):
            for x in range(width):
                dist = math.sqrt((x - center[0])**2 + (y - center[1])**2)
                t = min(dist / max_dist, 1.0)
                r = int(color1[0] + (color2[0] - color1[0]) * t)
                g = int(color1[1] + (color2[1] - color1[1]) * t)
                b = int(color1[2] + (color2[2] - color1[2]) * t)
                img.putpixel((x, y), (r, g, b))
        
        return img

class TextEffects:
    """Advanced text effects"""
    
    @staticmethod
    def draw_text_with_outline(draw: ImageDraw.ImageDraw,
                              position: Tuple[int, int],
                              text: str,
                              font: ImageFont.FreeTypeFont,
                              text_color: Tuple[int, int, int, int],
                              outline_color: Tuple[int, int, int, int],
                              outline_width: int = 2):
        """Draw text with outline effect"""
        x, y = position
        
        # Draw outline
        for adj_x in range(-outline_width, outline_width + 1):
            for adj_y in range(-outline_width, outline_width + 1):
                if adj_x != 0 or adj_y != 0:
                    draw.text((x + adj_x, y + adj_y), text, font=font, fill=outline_color)
        
        # Draw main text
        draw.text(position, text, font=font, fill=text_color)
    
    @staticmethod
    def draw_text_with_shadow(draw: ImageDraw.ImageDraw,
                            position: Tuple[int, int],
                            text: str,
                            font: ImageFont.FreeTypeFont,
                            text_color: Tuple[int, int, int, int],
                            shadow_color: Tuple[int, int, int, int],
                            shadow_offset: Tuple[int, int] = (3, 3)):
        """Draw text with shadow effect"""
        x, y = position
        
        # Draw shadow
        draw.text((x + shadow_offset[0], y + shadow_offset[1]), 
                 text, font=font, fill=shadow_color)
        
        # Draw main text
        draw.text(position, text, font=font, fill=text_color)
    
    @staticmethod
    def draw_text_with_glow(draw: ImageDraw.ImageDraw,
                          position: Tuple[int, int],
                          text: str,
                          font: ImageFont.FreeTypeFont,
                          text_color: Tuple[int, int, int, int],
                          glow_color: Tuple[int, int, int, int],
                          glow_radius: int = 5):
        """Draw text with glow effect"""
        x, y = position
        
        # Draw glow layers
        for i in range(glow_radius, 0, -1):
            alpha = int(100 * (glow_radius - i) / glow_radius)
            glow = (glow_color[0], glow_color[1], glow_color[2], alpha)
            for angle in range(0, 360, 30):
                rad = math.radians(angle)
                offset_x = int(i * math.cos(rad))
                offset_y = int(i * math.sin(rad))
                draw.text((x + offset_x, y + offset_y), text, font=font, fill=glow)
        
        # Draw main text
        draw.text(position, text, font=font, fill=text_color)
