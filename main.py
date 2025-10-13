#!/usr/bin/env python3
"""
Py-Magic-Canvas: Expert-Level Banner Designer
- Gradient background rendering using PIL
- Custom font support (falls back to system default)
- Dynamic text curve with adjustable semi-circle angle via Tkinter slider
- Shadow effect for text
- Optimized rendering pipeline with structured error handling

Author: py-magic-canvas contributors
Date: October 2025
"""
from __future__ import annotations

import math
import os
import sys
import traceback
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Tuple, List

from PIL import Image, ImageDraw, ImageFont, ImageTk


# ---------- Utilities ----------

def safe_int(value: str, default: int) -> int:
    try:
        return int(value)
    except Exception:
        return default


def load_font(preferred_path: Optional[str], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load a custom font if available, otherwise fall back to a system font.
    Tries common system fonts as fallback.
    """
    candidates: List[str] = []
    if preferred_path and os.path.exists(preferred_path):
        candidates.append(preferred_path)

    # Common cross-platform defaults
    candidates.extend([
        # Windows
        r"C:\\Windows\\Fonts\\SegoeUI.ttf",
        r"C:\\Windows\\Fonts\\arial.ttf",
        # macOS
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
        # Linux common paths
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ])

    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except Exception:
            continue

    # PIL default bitmap font (last resort)
    return ImageFont.load_default()


def create_linear_gradient(size: Tuple[int, int], start_color: Tuple[int, int, int], end_color: Tuple[int, int, int], vertical: bool = True) -> Image:
    """Create a smooth linear gradient with PIL without per-pixel Python loops.
    Uses resized 1px gradient band for performance.
    """
    w, h = size
    band_len = h if vertical else w
    base = Image.new("RGB", (1 if vertical else band_len, band_len if vertical else 1))
    draw = ImageDraw.Draw(base)

    # Draw band gradient
    for i in range(band_len):
        t = i / max(band_len - 1, 1)
        r = int(start_color[0] + (end_color[0] - start_color[0]) * t)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * t)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * t)
        if vertical:
            draw.point((0, i), fill=(r, g, b))
        else:
            draw.point((i, 0), fill=(r, g, b))

    gradient = base.resize((w, h))
    return gradient


def hex_to_rgb(hx: str) -> Tuple[int, int, int]:
    hx = hx.strip().lstrip('#')
    if len(hx) == 3:
        hx = ''.join(c * 2 for c in hx)
    if len(hx) != 6:
        return (0, 0, 0)
    return tuple(int(hx[i:i+2], 16) for i in (0, 2, 4))


# ---------- Core App ----------

class MagicCanvasApp:
    """Main application class for the Magic Canvas design tool.
    Provides a GUI for creating banner designs with curved text.
    """

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Py-Magic-Canvas - Banner Designer")
        self.root.geometry("1100x780")

        # Canvas dimensions
        self.canvas_width = 900
        self.canvas_height = 450

        # Default settings
        self.banner_text = "MAGIC CANVAS"
        self.text_color = "#ffffff"
        self.shadow_color = "#000000"
        self.bg_start_color = "#4ECDC4"
        self.bg_end_color = "#556270"
        self.font_size = 64
        self.arc_angle = 180  # degrees of the semi-circle arc
        self.curve_radius = 180
        self.font_path: Optional[str] = None
        self.gradient_vertical = True
        self.shadow_offset = (4, 4)
        self.shadow_blur = 0  # basic offset shadow (no blur dependency)

        # Rendering cache
        self.image: Optional[Image.Image] = None
        self.photo_image: Optional[ImageTk.PhotoImage] = None

        self._setup_ui()
        self._generate_preview()

    # ---------- UI ----------
    def _setup_ui(self) -> None:
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        # Left: Controls
        controls = ttk.Frame(main)
        controls.pack(side=tk.LEFT, fill=tk.Y)

        # Right: Preview
        preview = ttk.Frame(main)
        preview.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Controls: Text
        ttk.Label(controls, text="Banner Text").pack(anchor=tk.W)
        self.text_var = tk.StringVar(value=self.banner_text)
        text_entry = ttk.Entry(controls, textvariable=self.text_var, width=40)
        text_entry.pack(anchor=tk.W, pady=(0, 8))
        text_entry.bind("<KeyRelease>", lambda e: self._debounced_render())

        # Font size
        ttk.Label(controls, text="Font Size").pack(anchor=tk.W)
        self.font_size_var = tk.IntVar(value=self.font_size)
        ttk.Scale(controls, from_=16, to=140, orient=tk.HORIZONTAL, variable=self.font_size_var, command=lambda *_: self._debounced_render()).pack(fill=tk.X)

        # Arc angle (semi-circle sweep)
        ttk.Label(controls, text="Arc Angle (degrees)").pack(anchor=tk.W, pady=(8, 0))
        self.arc_angle_var = tk.IntVar(value=self.arc_angle)
        ttk.Scale(controls, from_=60, to=300, orient=tk.HORIZONTAL, variable=self.arc_angle_var, command=lambda *_: self._debounced_render()).pack(fill=tk.X)

        # Curve radius
        ttk.Label(controls, text="Curve Radius").pack(anchor=tk.W, pady=(8, 0))
        self.radius_var = tk.IntVar(value=self.curve_radius)
        ttk.Scale(controls, from_=80, to=400, orient=tk.HORIZONTAL, variable=self.radius_var, command=lambda *_: self._debounced_render()).pack(fill=tk.X)

        # Text color
        ttk.Label(controls, text="Text Color (hex)").pack(anchor=tk.W, pady=(8, 0))
        self.text_color_var = tk.StringVar(value=self.text_color)
        ttk.Entry(controls, textvariable=self.text_color_var).pack(fill=tk.X)

        # Shadow options
        ttk.Label(controls, text="Shadow Offset X,Y").pack(anchor=tk.W, pady=(8, 0))
        self.shadow_x_var = tk.IntVar(value=self.shadow_offset[0])
        self.shadow_y_var = tk.IntVar(value=self.shadow_offset[1])
        row = ttk.Frame(controls)
        row.pack(fill=tk.X)
        ttk.Entry(row, width=6, textvariable=self.shadow_x_var).pack(side=tk.LEFT)
        ttk.Entry(row, width=6, textvariable=self.shadow_y_var).pack(side=tk.LEFT, padx=(6, 0))

        # Gradient colors
        ttk.Label(controls, text="Gradient Start (hex)").pack(anchor=tk.W, pady=(8, 0))
        self.bg_start_var = tk.StringVar(value=self.bg_start_color)
        ttk.Entry(controls, textvariable=self.bg_start_var).pack(fill=tk.X)

        ttk.Label(controls, text="Gradient End (hex)").pack(anchor=tk.W, pady=(8, 0))
        self.bg_end_var = tk.StringVar(value=self.bg_end_color)
        ttk.Entry(controls, textvariable=self.bg_end_var).pack(fill=tk.X)

        # Gradient direction
        ttk.Label(controls, text="Gradient Direction").pack(anchor=tk.W, pady=(8, 0))
        self.grad_dir_var = tk.StringVar(value="Vertical")
        ttk.Combobox(controls, textvariable=self.grad_dir_var, values=["Vertical", "Horizontal"], state="readonly").pack(fill=tk.X)

        # Font path
        ttk.Label(controls, text="Custom Font Path (optional)").pack(anchor=tk.W, pady=(8, 0))
        self.font_path_var = tk.StringVar(value="")
        font_row = ttk.Frame(controls)
        font_row.pack(fill=tk.X)
        ttk.Entry(font_row, textvariable=self.font_path_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(font_row, text="Browse", command=self._browse_font).pack(side=tk.LEFT, padx=(6, 0))

        # Buttons
        ttk.Button(controls, text="Render", command=self._generate_preview).pack(fill=tk.X, pady=(12, 0))
        ttk.Button(controls, text="Export PNG", command=self._export_image).pack(fill=tk.X, pady=(6, 0))

        # Canvas preview using Tkinter Canvas with PhotoImage
        self.tk_canvas = tk.Canvas(preview, width=self.canvas_width, height=self.canvas_height, bg="#222222", highlightthickness=0)
        self.tk_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.root, textvariable=self.status_var, anchor=tk.W).pack(fill=tk.X, side=tk.BOTTOM)

    def _browse_font(self) -> None:
        path = filedialog.askopenfilename(title="Choose a .ttf/.otf font", filetypes=[("Font files", "*.ttf *.otf"), ("All files", "*.*")])
        if path:
            self.font_path_var.set(path)
            self._debounced_render()

    # ---------- Rendering ----------
    def _debounced_render(self):
        # Simple immediate render; hook for future debounce if needed
        self._generate_preview()

    def _generate_preview(self) -> None:
        try:
            # Pull current state from UI
            self.banner_text = self.text_var.get()
            self.font_size = int(self.font_size_var.get())
            self.arc_angle = int(self.arc_angle_var.get())
            self.curve_radius = int(self.radius_var.get())
            self.text_color = self.text_color_var.get()
            self.bg_start_color = self.bg_start_var.get()
            self.bg_end_color = self.bg_end_var.get()
            self.gradient_vertical = (self.grad_dir_var.get() == "Vertical")
            self.font_path = self.font_path_var.get() or None
            self.shadow_offset = (safe_int(str(self.shadow_x_var.get()), 4), safe_int(str(self.shadow_y_var.get()), 4))

            # Create base image with gradient background
            start_rgb = hex_to_rgb(self.bg_start_color)
            end_rgb = hex_to_rgb(self.bg_end_color)
            base = create_linear_gradient((self.canvas_width, self.canvas_height), start_rgb, end_rgb, vertical=self.gradient_vertical)

            # Render curved text with shadow
            self._draw_curved_text(base)

            # Optional decorative elements
            self._draw_decorations(base)

            # Update Tk preview efficiently
            self.image = base
            self._update_preview()
            self.status_var.set("Rendered successfully")
        except Exception as e:
            self.status_var.set("Render failed")
            traceback.print_exc()
            messagebox.showerror("Error", f"Rendering failed:\n{e}")

    def _update_preview(self) -> None:
        if self.image is None:
            return
        # Convert to PhotoImage once per frame
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.tk_canvas.delete("all")
        self.tk_canvas.create_image(self.canvas_width // 2, self.canvas_height // 2, image=self.photo_image)

    def _draw_curved_text(self, img: Image.Image) -> None:
        draw = ImageDraw.Draw(img)
        font = load_font(self.font_path, self.font_size)

        text = self.banner_text or ""
        if not text:
            return

        # Compute total arc length for spacing using font.getlength if available, else sum of widths
        try:
            total_width = font.getlength(text)  # type: ignore[attr-defined]
        except Exception:
            total_width = sum(font.getsize(c)[0] for c in text)

        # Arc geometry
        sweep_deg = max(10, min(360, self.arc_angle))  # clamp
        radius = max(20, self.curve_radius)
        center = (self.canvas_width // 2, self.canvas_height // 2 + radius // 3)
        # Convert width to arc angle using arc_len = theta(rad) * r
        theta_total = total_width / float(radius)
        theta_total_deg = math.degrees(theta_total)
        # Fit within desired sweep
        theta_deg = min(theta_total_deg, sweep_deg)

        # Starting angle so that text is centered on arc
        start_angle = -theta_deg / 2.0 - 90.0  # start from top going clockwise

        # Per-character placement by proportional width
        try:
            widths = [font.getlength(c) for c in text]  # type: ignore[attr-defined]
        except Exception:
            widths = [font.getsize(c)[0] for c in text]
        total_w = sum(widths) or 1

        acc = 0.0
        for idx, ch in enumerate(text):
            w = widths[idx]
            # angle for character center
            frac = (acc + w / 2.0) / total_w
            angle = start_angle + frac * theta_deg
            rad = math.radians(angle)

            # Point on circle
            cx = center[0] + radius * math.cos(rad)
            cy = center[1] + radius * math.sin(rad)

            # Render each glyph rotated: draw onto its own image for rotation
            glyph_img = Image.new("RGBA", (self.font_size * 2, self.font_size * 2), (0, 0, 0, 0))
            gdraw = ImageDraw.Draw(glyph_img)

            # Shadow
            sx, sy = self.shadow_offset
            gdraw.text((self.font_size + sx, self.font_size + sy), ch, font=font, fill=self.shadow_color)
            # Foreground
            gdraw.text((self.font_size, self.font_size), ch, font=font, fill=self.text_color)

            # Rotate so that baseline is tangent to circle (angle + 90)
            rot = glyph_img.rotate(angle + 90, resample=Image.BICUBIC, expand=True)
            gw, gh = rot.size
            img.paste(rot, (int(cx - gw / 2), int(cy - gh / 2)), rot)

            acc += w

    def _draw_decorations(self, img: Image.Image) -> None:
        draw = ImageDraw.Draw(img)
        # Subtle border
        border_color = (255, 255, 255)
        draw.rectangle([5, 5, self.canvas_width - 5, self.canvas_height - 5], outline=border_color, width=2)

    # ---------- Export ----------
    def _export_image(self) -> None:
        if self.image is None:
            messagebox.showwarning("Warning", "No image to export!")
            return
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
            )
            if file_path:
                # Convert to RGB for JPEG if needed
                out = self.image.convert("RGB") if file_path.lower().endswith((".jpg", ".jpeg")) else self.image
                out.save(file_path)
                messagebox.showinfo("Success", f"Image exported to:\n{file_path}")
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to export image:\n{e}")
