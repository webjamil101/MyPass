"""
Main window view for Password Manager
"""
import tkinter as tk
from tkinter import ttk
import logging
from .password_form import PasswordForm
from .password_list import PasswordList

logger = logging.getLogger(__name__)

class MainWindow:
    """Main application window"""
    
    def __init__(self, root, controller, responsive_vars):
        self.root = root
        self.controller = controller
        self.responsive_vars = responsive_vars
        
        # Initialize UI components
        self.password_form = None
        self.password_list = None
        self.status_var = None
        self.security_indicator = None
        
        # Setup window
        self.setup_window()
        
        # Create UI
        self.create_ui()
        
    def setup_window(self):
        """Configure main window"""
        self.root.title("MyPass - Secure Password Manager")
        
        # Set responsive window size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        window_width = min(int(screen_width * 0.8), 1400)
        window_height = min(int(screen_height * 0.8), 800)
        
        window_width = max(window_width, 800)
        window_height = max(window_height, 600)
        
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.configure(bg='#1e1e1e')
        self.root.resizable(True, True)
        
        # Center window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"+{x}+{y}")
        
        # Set icon if available
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
    def create_header(self, parent):
        """Create application header"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # Responsive font sizes
        is_small = self.responsive_vars['small'].get()
        is_medium = self.responsive_vars['medium'].get()
        
        title_font_size = 20 if is_small else (22 if is_medium else 24)
        subtitle_font_size = 10 if is_small else (11 if is_medium else 12)
        
        title_label = tk.Label(
            header_frame,
            text="MyPass",
            font=("Segoe UI", title_font_size, "bold"),
            bg='#1e1e1e',
            fg='#007acc'
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Secure Password Manager",
            font=("Segoe UI", subtitle_font_size),
            bg='#1e1e1e',
            fg='#cccccc'
        )
        subtitle_label.pack(side=tk.LEFT, padx=(8, 0), pady=4)
        
        # Security indicator
        security_frame = ttk.Frame(header_frame)
        security_frame.pack(side=tk.RIGHT)
        
        security_font_size = 9 if is_small else 10
        security_padx = 8 if is_small else 10
        
        self.security_indicator = tk.Label(
            security_frame,
            text="🔒 Encrypted",
            font=("Segoe UI", security_font_size),
            bg='#4CAF50',
            fg="white",
            padx=security_padx,
            pady=4,
            bd=0,
            relief="flat"
        )
        self.security_indicator.pack()
        
    def create_small_screen_layout(self, parent):
        """Create layout for small screens"""
        # Input form panel
        input_frame = ttk.LabelFrame(parent, text="Add New Password", padding=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        self.password_form = PasswordForm(input_frame, self.controller, self.responsive_vars, compact=True)
        
        # Password list panel
        list_frame = ttk.LabelFrame(parent, text="Saved Passwords", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        self.password_list = PasswordList(list_frame, self.controller, self.responsive_vars, compact=True)
        
    def create_large_screen_layout(self, parent):
        """Create layout for medium/large screens"""
        # Left panel - Input form
        left_panel = ttk.LabelFrame(parent, text="Add New Password", padding=15)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.password_form = PasswordForm(left_panel, self.controller, self.responsive_vars, compact=False)
        
        # Right panel - Password list
        right_panel = ttk.LabelFrame(parent, text="Saved Passwords", padding=15)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        self.password_list = PasswordList(right_panel, self.controller, self.responsive_vars, compact=False)
        
    def create_status_bar(self, parent):
        """Create status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        
        self.status_var = tk.StringVar(value="Ready")
        
        is_small = self.responsive_vars['small'].get()
        status_font_size = 9 if is_small else 10
        
        status_label = ttk.Label(
            status_frame, 
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Segoe UI", status_font_size)
        )
        status_label.pack(fill=tk.X)
        
    def create_ui(self):
        """Create user interface"""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Calculate responsive padding
        is_small = self.responsive_vars['small'].get()
        is_medium = self.responsive_vars['medium'].get()
        
        pad_x = 10 if is_small else (15 if is_medium else 20)
        pad_y = 10 if is_small else (15 if is_medium else 20)
        
        # Header - Now this method is defined before being called
        self.create_header(main_container)
        
        # Main content area
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=pad_x, pady=pad_y)
        
        # Create layout based on screen size
        if is_small:
            self.create_small_screen_layout(content_frame)
        else:
            self.create_large_screen_layout(content_frame)
        
        # Status bar
        self.create_status_bar(main_container)
        
    def update_status(self, message: str):
        """Update status bar message"""
        if self.status_var:
            self.status_var.set(message)
            self.root.after(5000, lambda: self.status_var.set("Ready") if self.status_var else None)
        
    def get_password_form(self):
        """Get password form instance"""
        return self.password_form
        
    def get_password_list(self):
        """Get password list instance"""
        return self.password_list