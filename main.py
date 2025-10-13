#!/usr/bin/env python3
"""
Py-Magic-Canvas: A Python tool for generating custom Canva-style design templates
This module demonstrates generating a semi-circle text design for a banner
using Tkinter for the frontend and PIL for image rendering.

Author: py-magic-canvas contributors
Date: October 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk
import math
import os


class MagicCanvasApp:
    """
    Main application class for the Magic Canvas design tool.
    Provides a GUI interface for creating custom banner designs with curved text.
    """
    
    def __init__(self, root):
        """
        Initialize the Magic Canvas application.
        
        Args:
            root: The Tkinter root window
        """
        self.root = root
        self.root.title("Py-Magic-Canvas - Banner Designer")
        self.root.geometry("1000x700")
        
        # Canvas dimensions
        self.canvas_width = 800
        self.canvas_height = 400
        
        # Default text settings
        self.banner_text = "MAGIC CANVAS"
        self.text_color = "#FF6B6B"
        self.bg_color = "#4ECDC4"
        self.font_size = 40
        
        # Create PIL Image for rendering
        self.image = None
        self.photo_image = None
        
        self._setup_ui()
        self._generate_preview()
    
    def _setup_ui(self):
        """
        Set up the user interface with controls and preview canvas.
        """
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Control panel (left side)
        control_frame = ttk.LabelFrame(main_frame, text="Design Controls", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Text input
        ttk.Label(control_frame, text="Banner Text:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.text_entry = ttk.Entry(control_frame, width=25)
        self.text_entry.insert(0, self.banner_text)
        self.text_entry.grid(row=0, column=1, pady=5)
        
        # Font size
        ttk.Label(control_frame, text="Font Size:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.font_size_var = tk.IntVar(value=self.font_size)
        font_scale = ttk.Scale(control_frame, from_=20, to=80, orient=tk.HORIZONTAL, 
                               variable=self.font_size_var, command=self._on_change)
        font_scale.grid(row=1, column=1, pady=5, sticky=(tk.W, tk.E))
        
        # Text color
        ttk.Label(control_frame, text="Text Color:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.text_color_entry = ttk.Entry(control_frame, width=25)
        self.text_color_entry.insert(0, self.text_color)
        self.text_color_entry.grid(row=2, column=1, pady=5)
        
        # Background color
        ttk.Label(control_frame, text="Background Color:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.bg_color_entry = ttk.Entry(control_frame, width=25)
        self.bg_color_entry.insert(0, self.bg_color)
        self.bg_color_entry.grid(row=3, column=1, pady=5)
        
        # Update button
        update_btn = ttk.Button(control_frame, text="Update Preview", command=self._update_preview)
        update_btn.grid(row=4, column=0, columnspan=2, pady=15)
        
        # Export button
        export_btn = ttk.Button(control_frame, text="Export as PNG", command=self._export_image)
        export_btn.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Instructions
        instructions = (
            "Instructions:\n\n"
            "1. Enter your text\n"
            "2. Adjust font size\n"
            "3. Set colors (hex format)\n"
            "4. Click 'Update Preview'\n"
            "5. Export when satisfied"
        )
        ttk.Label(control_frame, text=instructions, justify=tk.LEFT, 
                 foreground="#666").grid(row=6, column=0, columnspan=2, pady=20, sticky=tk.W)
        
        # Preview canvas (right side)
        preview_frame = ttk.LabelFrame(main_frame, text="Live Preview", padding="10")
        preview_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.canvas = tk.Canvas(preview_frame, width=self.canvas_width, 
                                height=self.canvas_height, bg="white")
        self.canvas.pack()
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
    
    def _on_change(self, event=None):
        """
        Handle real-time slider changes.
        
        Args:
            event: The event object (optional)
        """
        self.font_size = int(self.font_size_var.get())
        self._generate_preview()
    
    def _update_preview(self):
        """
        Update the preview with new text and color settings.
        """
        try:
            self.banner_text = self.text_entry.get() or "MAGIC CANVAS"
            self.text_color = self.text_color_entry.get() or "#FF6B6B"
            self.bg_color = self.bg_color_entry.get() or "#4ECDC4"
            self.font_size = int(self.font_size_var.get())
            
            self._generate_preview()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    def _generate_preview(self):
        """
        Generate the banner preview with semi-circular text arrangement.
        Uses PIL for high-quality rendering.
        """
        # Create a new image with the background color
        self.image = Image.new('RGB', (self.canvas_width, self.canvas_height), self.bg_color)
        draw = ImageDraw.Draw(self.image)
        
        # Try to use a nice font, fall back to default if not available
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 
                                      self.font_size)
        except:
            try:
                # Try Windows font path
                font = ImageFont.truetype("C:/Windows/Fonts/Arial.ttf", self.font_size)
            except:
                # Fall back to default font
                font = ImageFont.load_default()
        
        # Calculate semi-circle parameters
        center_x = self.canvas_width // 2
        center_y = self.canvas_height // 2
        radius = 150  # Radius of the semi-circle
        
        # Calculate angle span for text
        text_length = len(self.banner_text)
        angle_step = 180 / (text_length + 1)  # Divide semi-circle among characters
        
        # Draw each character along the semi-circle arc
        for i, char in enumerate(self.banner_text):
            # Calculate angle for this character (180 degrees = π radians for semi-circle)
            angle = math.radians(180 - (i + 1) * angle_step)
            
            # Calculate position on the arc
            x = center_x + radius * math.cos(angle)
            y = center_y - radius * math.sin(angle)  # Subtract to go upward
            
            # Get character size for centering
            bbox = draw.textbbox((0, 0), char, font=font)
            char_width = bbox[2] - bbox[0]
            char_height = bbox[3] - bbox[1]
            
            # Adjust position to center the character
            x -= char_width / 2
            y -= char_height / 2
            
            # Draw the character
            draw.text((x, y), char, fill=self.text_color, font=font)
        
        # Add decorative elements
        self._add_decorative_elements(draw)
        
        # Convert PIL Image to PhotoImage for Tkinter
        self.photo_image = ImageTk.PhotoImage(self.image)
        
        # Update canvas
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
    
    def _add_decorative_elements(self, draw):
        """
        Add decorative elements to enhance the banner design.
        
        Args:
            draw: ImageDraw object for drawing
        """
        # Add a subtle border
        border_color = "#2C3E50"
        draw.rectangle([5, 5, self.canvas_width-5, self.canvas_height-5], 
                       outline=border_color, width=3)
        
        # Add corner accents
        accent_size = 20
        for corner in [(10, 10), (self.canvas_width-10, 10), 
                       (10, self.canvas_height-10), (self.canvas_width-10, self.canvas_height-10)]:
            x, y = corner
            # Draw small decorative circles
            draw.ellipse([x-5, y-5, x+5, y+5], fill=self.text_color)
    
    def _export_image(self):
        """
        Export the current design as a PNG file.
        Opens a file dialog for the user to choose save location.
        """
        if self.image is None:
            messagebox.showwarning("Warning", "No image to export!")
            return
        
        try:
            # Open file dialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            
            if file_path:
                # Save the image
                self.image.save(file_path)
                messagebox.showinfo("Success", f"Image exported successfully to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export image: {str(e)}")


def main():
    """
    Main entry point for the application.
    Creates and runs the Tkinter application.
    """
    root = tk.Tk()
    app = MagicCanvasApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
