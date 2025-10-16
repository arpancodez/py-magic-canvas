#!/usr/bin/env python3
"""UI Components for py-magic-canvas

This module provides enhanced UI components for Tkinter:
- Custom styled buttons
- Color pickers
- Slider controls
- Tool panels
- Property inspectors
"""

import tkinter as tk
from tkinter import ttk, colorchooser
from typing import Callable, Optional, Tuple

class StyledButton(tk.Button):
    """Custom styled button with hover effects"""
    
    def __init__(self, parent, text="", command=None, **kwargs):
        # Default styling
        default_style = {
            'bg': '#4CAF50',
            'fg': 'white',
            'font': ('Arial', 10, 'bold'),
            'relief': tk.FLAT,
            'padx': 20,
            'pady': 10,
            'cursor': 'hand2'
        }
        # Merge with user kwargs
        default_style.update(kwargs)
        
        super().__init__(parent, text=text, command=command, **default_style)
        
        # Store colors for hover effect
        self.default_bg = default_style.get('bg', '#4CAF50')
        self.hover_bg = self._darken_color(self.default_bg)
        
        # Bind hover events
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
    
    def _darken_color(self, color: str) -> str:
        """Darken a color for hover effect"""
        # Simple darkening - can be improved
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            r = max(0, r - 30)
            g = max(0, g - 30)
            b = max(0, b - 30)
            return f'#{r:02x}{g:02x}{b:02x}'
        return color
    
    def _on_enter(self, event):
        self.config(bg=self.hover_bg)
    
    def _on_leave(self, event):
        self.config(bg=self.default_bg)

class ColorPicker(tk.Frame):
    """Color picker component"""
    
    def __init__(self, parent, initial_color='#000000', on_change: Optional[Callable] = None):
        super().__init__(parent)
        
        self.color = initial_color
        self.on_change = on_change
        
        # Color display
        self.color_display = tk.Canvas(self, width=50, height=30, bg=self.color)
        self.color_display.pack(side=tk.LEFT, padx=5)
        
        # Hex label
        self.color_label = tk.Label(self, text=self.color, width=10)
        self.color_label.pack(side=tk.LEFT, padx=5)
        
        # Pick button
        self.pick_button = tk.Button(self, text="Pick", command=self._pick_color)
        self.pick_button.pack(side=tk.LEFT, padx=5)
    
    def _pick_color(self):
        color = colorchooser.askcolor(initialcolor=self.color)
        if color[1]:
            self.set_color(color[1])
    
    def set_color(self, color: str):
        self.color = color
        self.color_display.config(bg=color)
        self.color_label.config(text=color)
        if self.on_change:
            self.on_change(color)
    
    def get_color(self) -> str:
        return self.color

class SliderControl(tk.Frame):
    """Labeled slider control"""
    
    def __init__(self, parent, label="", from_=0, to=100, initial=50, 
                 on_change: Optional[Callable] = None):
        super().__init__(parent)
        
        self.on_change = on_change
        
        # Label
        self.label = tk.Label(self, text=label, width=15, anchor='w')
        self.label.pack(side=tk.LEFT, padx=5)
        
        # Slider
        self.slider = tk.Scale(self, from_=from_, to=to, orient=tk.HORIZONTAL,
                              command=self._on_slider_change, length=200)
        self.slider.set(initial)
        self.slider.pack(side=tk.LEFT, padx=5)
        
        # Value display
        self.value_label = tk.Label(self, text=str(initial), width=5)
        self.value_label.pack(side=tk.LEFT, padx=5)
    
    def _on_slider_change(self, value):
        self.value_label.config(text=value)
        if self.on_change:
            self.on_change(float(value))
    
    def get_value(self) -> float:
        return self.slider.get()
    
    def set_value(self, value: float):
        self.slider.set(value)

class ToolPanel(tk.LabelFrame):
    """Tool panel with buttons"""
    
    def __init__(self, parent, title="Tools"):
        super().__init__(parent, text=title, padx=10, pady=10)
        self.tools = {}
        self.selected_tool = None
    
    def add_tool(self, name: str, icon: str, command: Callable):
        """Add a tool button"""
        btn = tk.Button(self, text=icon, command=lambda: self._select_tool(name, command),
                       width=8, height=2)
        btn.pack(pady=5, fill=tk.X)
        self.tools[name] = btn
        return btn
    
    def _select_tool(self, name: str, command: Callable):
        # Deselect previous
        if self.selected_tool and self.selected_tool in self.tools:
            self.tools[self.selected_tool].config(relief=tk.RAISED)
        
        # Select new
        self.selected_tool = name
        self.tools[name].config(relief=tk.SUNKEN)
        
        # Execute command
        command()
    
    def get_selected_tool(self) -> Optional[str]:
        return self.selected_tool

class PropertyInspector(tk.LabelFrame):
    """Property inspector panel"""
    
    def __init__(self, parent, title="Properties"):
        super().__init__(parent, text=title, padx=10, pady=10)
        self.properties = {}
    
    def add_property(self, name: str, widget_type: str, **kwargs):
        """Add a property control"""
        frame = tk.Frame(self)
        frame.pack(fill=tk.X, pady=5)
        
        # Label
        label = tk.Label(frame, text=name + ":", width=12, anchor='w')
        label.pack(side=tk.LEFT)
        
        # Widget
        if widget_type == 'entry':
            widget = tk.Entry(frame, **kwargs)
        elif widget_type == 'spinbox':
            widget = tk.Spinbox(frame, **kwargs)
        elif widget_type == 'combobox':
            widget = ttk.Combobox(frame, **kwargs)
        elif widget_type == 'checkbox':
            widget = tk.Checkbutton(frame, **kwargs)
        else:
            widget = tk.Entry(frame)
        
        widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.properties[name] = widget
        
        return widget
    
    def get_property(self, name: str):
        """Get property value"""
        if name in self.properties:
            widget = self.properties[name]
            if isinstance(widget, (tk.Entry, tk.Spinbox)):
                return widget.get()
            elif isinstance(widget, ttk.Combobox):
                return widget.get()
            elif isinstance(widget, tk.Checkbutton):
                return widget.var.get() if hasattr(widget, 'var') else None
        return None
    
    def set_property(self, name: str, value):
        """Set property value"""
        if name in self.properties:
            widget = self.properties[name]
            if isinstance(widget, (tk.Entry, tk.Spinbox)):
                widget.delete(0, tk.END)
                widget.insert(0, str(value))
            elif isinstance(widget, ttk.Combobox):
                widget.set(value)

class Toolbar(tk.Frame):
    """Toolbar with buttons and separators"""
    
    def __init__(self, parent):
        super().__init__(parent, relief=tk.RAISED, bd=2)
        self.pack(side=tk.TOP, fill=tk.X)
    
    def add_button(self, text: str, command: Callable, icon: str = ""):
        """Add a button to the toolbar"""
        display_text = icon if icon else text
        btn = tk.Button(self, text=display_text, command=command, relief=tk.FLAT,
                       padx=10, pady=5)
        btn.pack(side=tk.LEFT, padx=2, pady=2)
        return btn
    
    def add_separator(self):
        """Add a separator to the toolbar"""
        sep = tk.Frame(self, width=2, bg='gray', relief=tk.SUNKEN)
        sep.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        return sep

class StatusBar(tk.Frame):
    """Status bar for displaying information"""
    
    def __init__(self, parent):
        super().__init__(parent, relief=tk.SUNKEN, bd=1)
        self.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.label = tk.Label(self, text="Ready", anchor='w')
        self.label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def set_text(self, text: str):
        """Update status bar text"""
        self.label.config(text=text)
    
    def clear(self):
        """Clear status bar"""
        self.set_text("Ready")
