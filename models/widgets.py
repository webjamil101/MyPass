"""
Custom widgets for Password Manager
"""
import tkinter as tk
from tkinter import ttk

class EmailPlaceholderEntry(ttk.Entry):
    """Custom Entry widget with placeholder functionality"""
    
    def __init__(self, parent, placeholder_text="Enter email or username", **kwargs):
        super().__init__(parent, **kwargs)
        self.placeholder_text = placeholder_text
        self.placeholder_color = '#888888'
        self.normal_color = '#ffffff'
        
        self.insert(0, self.placeholder_text)
        self.configure(foreground=self.placeholder_color)
        
        self.bind('<FocusIn>', self._on_focus_in)
        self.bind('<FocusOut>', self._on_focus_out)
    
    def _on_focus_in(self, event):
        """Handle focus in event"""
        if self.get() == self.placeholder_text:
            self.delete(0, tk.END)
            self.configure(foreground=self.normal_color)
    
    def _on_focus_out(self, event):
        """Handle focus out event"""
        if not self.get().strip():
            self.insert(0, self.placeholder_text)
            self.configure(foreground=self.placeholder_color)
    
    def clear(self):
        """Clear the entry and show placeholder"""
        self.delete(0, tk.END)
        self.insert(0, self.placeholder_text)
        self.configure(foreground=self.placeholder_color)
    
    def set_text(self, text):
        """Set text without placeholder"""
        self.delete(0, tk.END)
        self.insert(0, text)
        self.configure(foreground=self.normal_color)
    
    def get_value(self):
        """Get value, returning empty string if it's placeholder text"""
        value = self.get()
        return "" if value == self.placeholder_text else value