"""
Responsive layout utilities for Password Manager
"""
import tkinter as tk
from typing import Dict, Callable

class ResponsiveHelper:
    """Helper for responsive layouts"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        
        # Responsive breakpoints
        self.breakpoints = {
            'small': 1024,
            'medium': 1280,
            'large': 1920
        }
        
        # Responsive variables
        self.responsive_vars = {
            'small': tk.BooleanVar(value=False),
            'medium': tk.BooleanVar(value=False),
            'large': tk.BooleanVar(value=False)
        }
        
        # Callbacks for responsive updates
        self.update_callbacks = []
        
    def get_responsive_vars(self) -> Dict[str, tk.BooleanVar]:
        """Get responsive variables"""
        return self.responsive_vars
        
    def update_responsive_vars(self):
        """Update responsive variables based on current window size"""
        try:
            current_width = self.root.winfo_width()
            if current_width < 1:
                current_width = self.screen_width
                
            # Update responsive variables
            self.responsive_vars['small'].set(current_width < self.breakpoints['small'])
            self.responsive_vars['medium'].set(
                self.breakpoints['small'] <= current_width < self.breakpoints['medium']
            )
            self.responsive_vars['large'].set(current_width >= self.breakpoints['medium'])
            
            # Notify callbacks
            for callback in self.update_callbacks:
                try:
                    callback()
                except:
                    pass
                    
        except Exception as e:
            # Window might be destroyed
            pass
            
    def add_update_callback(self, callback: Callable):
        """Add callback for responsive updates"""
        self.update_callbacks.append(callback)
        
    def start_updates(self):
        """Start responsive updates"""
        self.update_responsive_vars()
        self.root.after(100, self._schedule_update)
        
    def _schedule_update(self):
        """Schedule next update"""
        if self.root.winfo_exists():
            self.update_responsive_vars()
            self.root.after(500, self._schedule_update)
            
    def stop_updates(self):
        """Stop responsive updates"""
        self.update_callbacks.clear()