"""
Password form view for Password Manager
"""
import tkinter as tk
from tkinter import ttk
import pyperclip
from models.widgets import EmailPlaceholderEntry
import logging

logger = logging.getLogger(__name__)

class PasswordForm:
    """Password input form view"""
    
    def __init__(self, parent, controller, responsive_vars, compact=False):
        self.parent = parent
        self.controller = controller
        self.responsive_vars = responsive_vars
        self.compact = compact
        
        # Store default symbols and numbers
        self.default_symbols = None
        self.default_numbers = None
        
        self.create_form()
        
    def create_form(self):
        """Create password input form"""
        # Responsive settings
        entry_width = 25 if self.compact else 30
        label_padx = (0, 8) if self.compact else (0, 10)
        field_pady = 6 if self.compact else 8
        
        # Website
        website_frame = ttk.Frame(self.parent)
        website_frame.pack(fill=tk.X, pady=field_pady)
        
        ttk.Label(website_frame, text="Website:").pack(side=tk.LEFT, padx=label_padx)
        self.website_entry = ttk.Entry(website_frame, width=entry_width)
        self.website_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.website_entry.focus()
        
        # Category
        category_frame = ttk.Frame(self.parent)
        category_frame.pack(fill=tk.X, pady=field_pady)
        
        ttk.Label(category_frame, text="Category:").pack(side=tk.LEFT, padx=label_padx)
        self.category_var = tk.StringVar(value="General")
        category_values = ["General", "Social Media", "Email", "Banking", "Work", "Personal"]
        self.category_combo = ttk.Combobox(
            category_frame, 
            textvariable=self.category_var,
            values=category_values,
            state="readonly",
            width=entry_width - 2
        )
        self.category_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Email/Username with placeholder
        email_frame = ttk.Frame(self.parent)
        email_frame.pack(fill=tk.X, pady=field_pady)
        
        ttk.Label(email_frame, text="Email/Username:").pack(side=tk.LEFT, padx=label_padx)
        self.email_entry = EmailPlaceholderEntry(
            email_frame,
            placeholder_text="Enter email or username",
            width=entry_width
        )
        self.email_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Password
        password_frame = ttk.Frame(self.parent)
        password_frame.pack(fill=tk.X, pady=field_pady)
        
        ttk.Label(password_frame, text="Password:").pack(side=tk.LEFT, padx=label_padx)
        self.password_entry = ttk.Entry(password_frame, width=entry_width, show="•")
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Show/Hide password toggle
        self.show_password_var = tk.BooleanVar(value=False)
        self.show_password_btn = ttk.Checkbutton(
            password_frame, 
            text="Show", 
            variable=self.show_password_var,
            command=self.toggle_password_visibility,
            width=6 if self.compact else 8
        )
        self.show_password_btn.pack(side=tk.RIGHT, padx=(8, 0))
        
        # Password strength indicator
        self.strength_var = tk.StringVar(value="Strength: -")
        self.strength_label = ttk.Label(password_frame, textvariable=self.strength_var)
        self.strength_label.pack(side=tk.RIGHT, padx=(8, 0))
        self.password_entry.bind('<KeyRelease>', self.check_password_strength)
        
        # Password generation options
        self.create_generation_section(field_pady, label_padx)
        
        # Buttons
        self.create_buttons()
        
    def create_generation_section(self, field_pady, label_padx):
        """Create password generation section"""
        gen_frame = ttk.Frame(self.parent)
        gen_frame.pack(fill=tk.X, pady=field_pady)
        
        ttk.Label(gen_frame, text="Length:").pack(side=tk.LEFT, padx=label_padx)
        self.length_var = tk.IntVar(value=16)
        self.length_spin = ttk.Spinbox(gen_frame, from_=8, to=50, textvariable=self.length_var, width=4)
        self.length_spin.pack(side=tk.LEFT)
        
        # Store checkbox variables
        self.use_symbols = tk.BooleanVar(value=True)
        self.use_numbers = tk.BooleanVar(value=True)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        
        # Checkbutton layout based on screen size
        if self.compact:
            checkbox_frame = ttk.Frame(gen_frame)
            checkbox_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
            
            row1 = ttk.Frame(checkbox_frame)
            row1.pack(fill=tk.X)
            ttk.Checkbutton(row1, text="Symbols", variable=self.use_symbols).pack(side=tk.LEFT, padx=(0, 5))
            ttk.Checkbutton(row1, text="Numbers", variable=self.use_numbers).pack(side=tk.LEFT, padx=(0, 5))
            
            row2 = ttk.Frame(checkbox_frame)
            row2.pack(fill=tk.X, pady=(5, 0))
            ttk.Checkbutton(row2, text="Uppercase", variable=self.use_uppercase).pack(side=tk.LEFT, padx=(0, 5))
            ttk.Checkbutton(row2, text="Lowercase", variable=self.use_lowercase).pack(side=tk.LEFT, padx=(0, 5))
        else:
            ttk.Checkbutton(gen_frame, text="Symbols", variable=self.use_symbols).pack(side=tk.LEFT, padx=(10, 5))
            ttk.Checkbutton(gen_frame, text="Numbers", variable=self.use_numbers).pack(side=tk.LEFT, padx=(0, 5))
            ttk.Checkbutton(gen_frame, text="Uppercase", variable=self.use_uppercase).pack(side=tk.LEFT, padx=(0, 5))
            ttk.Checkbutton(gen_frame, text="Lowercase", variable=self.use_lowercase).pack(side=tk.LEFT, padx=(0, 5))
        
        # Custom symbols and numbers (only for larger screens)
        if not self.compact:
            self.create_custom_symbols_section(field_pady)
            
    def create_custom_symbols_section(self, field_pady):
        """Create custom symbols and numbers section"""
        # Get defaults from controller
        self.default_symbols = self.controller.get_default_symbols()
        self.default_numbers = self.controller.get_default_numbers()
        
        # Symbols customization
        symbols_frame = ttk.LabelFrame(self.parent, text="Custom Symbols", padding=10)
        symbols_frame.pack(fill=tk.X, pady=field_pady)
        
        self.custom_symbols_var = tk.StringVar(value=self.default_symbols)
        
        ttk.Label(symbols_frame, text="Symbols to use:").pack(anchor=tk.W)
        
        symbols_entry_frame = ttk.Frame(symbols_frame)
        symbols_entry_frame.pack(fill=tk.X, pady=5)
        
        self.symbols_entry = ttk.Entry(symbols_entry_frame, textvariable=self.custom_symbols_var, width=40)
        self.symbols_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(
            symbols_entry_frame, 
            text="Reset", 
            command=self.reset_symbols_to_default,
            width=8
        ).pack(side=tk.RIGHT, padx=(8, 0))
        
        # Numbers customization
        numbers_frame = ttk.LabelFrame(self.parent, text="Custom Numbers", padding=10)
        numbers_frame.pack(fill=tk.X, pady=field_pady)
        
        self.custom_numbers_var = tk.StringVar(value=self.default_numbers)
        
        ttk.Label(numbers_frame, text="Numbers to use:").pack(anchor=tk.W)
        
        numbers_entry_frame = ttk.Frame(numbers_frame)
        numbers_entry_frame.pack(fill=tk.X, pady=5)
        
        self.numbers_entry = ttk.Entry(numbers_entry_frame, textvariable=self.custom_numbers_var, width=40)
        self.numbers_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(
            numbers_entry_frame, 
            text="Reset", 
            command=self.reset_numbers_to_default,
            width=8
        ).pack(side=tk.RIGHT, padx=(8, 0))
        
    def create_buttons(self):
        """Create form buttons"""
        button_frame = ttk.Frame(self.parent)
        button_frame.pack(fill=tk.X, pady=15)
        
        button_width = 12 if self.compact else 15
        
        if self.compact:
            # Stack buttons vertically for small screens
            ttk.Button(
                button_frame, 
                text="Generate Password", 
                command=self.generate_advanced_password,
                style="Accent.TButton",
                width=button_width
            ).pack(fill=tk.X, pady=2)
            
            ttk.Button(
                button_frame, 
                text="Add Password", 
                command=self.save_password,
                style="Success.TButton",
                width=button_width
            ).pack(fill=tk.X, pady=2)
            
            ttk.Button(
                button_frame, 
                text="Search Website", 
                command=self.search_password,
                style="Accent.TButton",
                width=button_width
            ).pack(fill=tk.X, pady=2)
            
            ttk.Button(
                button_frame, 
                text="Clear Form", 
                command=self.clear_form,
                style="Danger.TButton",
                width=button_width
            ).pack(fill=tk.X, pady=2)
            
            ttk.Button(
                button_frame, 
                text="Show All", 
                command=self.show_all_passwords,
                width=button_width
            ).pack(fill=tk.X, pady=2)
        else:
            # Horizontal layout for larger screens
            ttk.Button(
                button_frame, 
                text="Generate Password", 
                command=self.generate_advanced_password,
                style="Accent.TButton",
                width=button_width
            ).pack(side=tk.LEFT, padx=(0, 8))
            
            ttk.Button(
                button_frame, 
                text="Add Password", 
                command=self.save_password,
                style="Success.TButton",
                width=button_width
            ).pack(side=tk.LEFT, padx=(0, 8))
            
            ttk.Button(
                button_frame, 
                text="Search Website", 
                command=self.search_password,
                style="Accent.TButton",
                width=button_width
            ).pack(side=tk.LEFT, padx=(0, 8))
            
            ttk.Button(
                button_frame, 
                text="Clear Form", 
                command=self.clear_form,
                style="Danger.TButton",
                width=button_width
            ).pack(side=tk.LEFT, padx=(0, 8))
            
            ttk.Button(
                button_frame, 
                text="Show All", 
                command=self.show_all_passwords,
                width=button_width
            ).pack(side=tk.RIGHT)
    
    # Enhanced methods
    def generate_advanced_password(self):
        """Generate password using controller with advanced options"""
        try:
            # Get custom symbols/number values
            custom_symbols = self.get_custom_symbols()
            custom_numbers = self.get_custom_numbers()
            
            generated = self.controller.generate_advanced_password(
                length=self.length_var.get(),
                use_lowercase=self.use_lowercase.get(),
                use_uppercase=self.use_uppercase.get(),
                use_numbers=self.use_numbers.get(),
                use_symbols=self.use_symbols.get(),
                custom_symbols=custom_symbols,
                custom_numbers=custom_numbers
            )
            
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, generated)
            self.check_password_strength()
            
            # Copy to clipboard
            pyperclip.copy(generated)
            self.controller.show_popup_message("Password generated and copied to clipboard!")
            
        except Exception as e:
            logger.error(f"Failed to generate password: {e}")
            self.controller.show_popup_message(f"Error generating password: {str(e)}", is_error=True)
    
    def get_custom_symbols(self):
        """Get custom symbols, fallback to default if empty"""
        if hasattr(self, 'custom_symbols_var'):
            custom_symbols = self.custom_symbols_var.get().strip()
            if custom_symbols:
                return custom_symbols
        return self.controller.get_default_symbols()
    
    def get_custom_numbers(self):
        """Get custom numbers, fallback to default if empty"""
        if hasattr(self, 'custom_numbers_var'):
            custom_numbers = self.custom_numbers_var.get().strip()
            if custom_numbers:
                return custom_numbers
        return self.controller.get_default_numbers()
    
    def reset_symbols_to_default(self):
        """Reset symbols to default"""
        if self.default_symbols:
            self.custom_symbols_var.set(self.default_symbols)
    
    def reset_numbers_to_default(self):
        """Reset numbers to default"""
        if self.default_numbers:
            self.custom_numbers_var.set(self.default_numbers)
    
    # Existing methods
    def save_password(self):
        """Save password using controller"""
        website = self.website_entry.get().strip()
        category = self.category_var.get()
        email = self.email_entry.get_value().strip()
        password = self.password_entry.get().strip()
        
        try:
            success, message = self.controller.save_password(
                website=website,
                email=email,
                password=password,
                category=category
            )
            
            if success:
                self.controller.show_popup_message(message)
                self.clear_form()
                self.controller.refresh_password_list()
            else:
                self.controller.show_popup_message(message, is_error=True)
                
        except Exception as e:
            logger.error(f"Failed to save password: {e}")
            self.controller.show_popup_message(f"Error saving password: {str(e)}", is_error=True)
    
    def search_password(self):
        """Search passwords using controller"""
        search_term = self.website_entry.get().strip()
        if search_term:
            self.controller.search_passwords(search_term)
    
    def show_all_passwords(self):
        """Show all passwords using controller"""
        self.controller.refresh_password_list()
        self.website_entry.focus_set()
    
    def clear_form(self):
        """Clear the form"""
        self.website_entry.delete(0, tk.END)
        self.category_var.set("General")
        self.email_entry.clear()
        self.password_entry.delete(0, tk.END)
        self.show_password_var.set(False)
        self.toggle_password_visibility()
        self.strength_var.set("Strength: -")
        self.website_entry.focus_set()
        
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="•")
    
    def check_password_strength(self, event=None):
        """Check password strength"""
        password = self.password_entry.get()
        if password:
            level, color, score = self.controller.check_password_strength(password)
            self.strength_var.set(f"Strength: {level}")
            self.strength_label.config(foreground=color)
        else:
            self.strength_var.set("Strength: -")
            self.strength_label.config(foreground='black')