"""
Theme and styling for Password Manager
"""
import tkinter as tk
from tkinter import ttk

def apply_theme(root):
    """Apply theme to the application"""
    # Create styles
    create_styles()
    
    # Configure root window
    root.configure(bg='#1e1e1e')
    
    # Set ttk theme
    style = ttk.Style()
    
    # Try to use clam theme for better customization
    available_themes = style.theme_names()
    if 'clam' in available_themes:
        style.theme_use('clam')
    
    # Configure styles
    style.configure('TFrame', background='#1e1e1e')
    style.configure('TLabel', background='#1e1e1e', foreground='#ffffff')
    style.configure('TLabelframe', background='#1e1e1e', foreground='#007acc')
    style.configure('TLabelframe.Label', background='#1e1e1e', foreground='#007acc')
    
    # Configure Treeview
    style.configure('Treeview',
                   background='#2d2d2d',
                   foreground='#ffffff',
                   fieldbackground='#2d2d2d',
                   rowheight=25)
    
    style.configure('Treeview.Heading',
                   background='#007acc',
                   foreground='#ffffff',
                   relief='flat')
    
    style.map('Treeview',
              background=[('selected', '#007acc')],
              foreground=[('selected', '#ffffff')])
    
    # Configure Buttons
    style.configure('TButton',
                   background='#333333',
                   foreground='#ffffff',
                   borderwidth=1,
                   focusthickness=3,
                   focuscolor='none')
    
    style.map('TButton',
              background=[('active', '#444444')],
              foreground=[('active', '#ffffff')])
    
    # Configure custom button styles
    style.configure('Success.TButton',
                   background='#4CAF50',
                   foreground='#ffffff')
    
    style.map('Success.TButton',
              background=[('active', '#45a049')],
              foreground=[('active', '#ffffff')])
    
    style.configure('Danger.TButton',
                   background='#f44336',
                   foreground='#ffffff')
    
    style.map('Danger.TButton',
              background=[('active', '#da190b')],
              foreground=[('active', '#ffffff')])
    
    style.configure('Accent.TButton',
                   background='#007acc',
                   foreground='#ffffff')
    
    style.map('Accent.TButton',
              background=[('active', '#005fa3')],
              foreground=[('active', '#ffffff')])
    
    # Configure Entry
    style.configure('TEntry',
                   fieldbackground='#2d2d2d',
                   foreground='#ffffff',
                   insertcolor='#ffffff',
                   borderwidth=1)
    
    # Configure Combobox
    style.configure('TCombobox',
                   fieldbackground='#2d2d2d',
                   foreground='#ffffff',
                   background='#2d2d2d')
    
    # Configure Spinbox
    style.configure('TSpinbox',
                   fieldbackground='#2d2d2d',
                   foreground='#ffffff',
                   background='#2d2d2d')
    
    # Configure Checkbutton
    style.configure('TCheckbutton',
                   background='#1e1e1e',
                   foreground='#ffffff')
    
    # Configure Scrollbar
    style.configure('TScrollbar',
                   background='#333333',
                   troughcolor='#1e1e1e',
                   borderwidth=0,
                   relief='flat')

def create_styles():
    """Create custom styles"""
    style = ttk.Style()
    
    # Add custom styles for different themes
    try:
        # Tooltip style
        style.configure('Tooltip.TLabel',
                       background='#ffffe0',
                       foreground='#000000',
                       relief='solid',
                       borderwidth=1,
                       padding=5)
        
        # Status bar style
        style.configure('Status.TLabel',
                       background='#007acc',
                       foreground='#ffffff',
                       relief='sunken',
                       padding=5)
        
    except Exception:
        # Fallback if style configuration fails
        pass