"""
Dialog windows for Password Manager
"""
import tkinter as tk
from tkinter import ttk
import pyperclip
import logging

logger = logging.getLogger(__name__)

class DuplicateDialog:
    """Dialog for handling duplicate passwords"""
    
    def __init__(self, parent, controller, duplicate_info):
        self.parent = parent
        self.controller = controller
        self.duplicate_info = duplicate_info
        
        self.result = None
        
        self.create_dialog()
        
    def create_dialog(self):
        """Create duplicate dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Duplicate Entry Detected")
        self.dialog.resizable(False, False)
        
        # Center dialog
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        x = self.parent.winfo_rootx() + 50
        y = self.parent.winfo_rooty() + 50
        self.dialog.geometry(f"+{x}+{y}")
        
        # Content frame
        content_frame = ttk.Frame(self.dialog, padding=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Message
        exact_match, duplicates = self.duplicate_info
        
        message = "An entry already exists with the same website and email.\n\n"
        message += f"Website: {exact_match['website']}\n"
        message += f"Email: {exact_match['email']}\n"
        message += f"Category: {exact_match['category']}\n"
        message += f"Date Added: {exact_match['date_added']}\n\n"
        
        if duplicates:
            message += "Similar entries:\n"
            for dup in duplicates:
                message += f"- {dup['website']} ({dup['email']})\n"
                
        message += "\nWhat would you like to do?"
        
        ttk.Label(
            content_frame, 
            text=message,
            justify=tk.LEFT,
            wraplength=400
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Buttons frame
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            button_frame,
            text="Overwrite Existing",
            command=self.overwrite,
            style="Danger.TButton",
            width=15
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="Create New Entry",
            command=self.create_new,
            style="Accent.TButton",
            width=15
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel,
            width=15
        ).pack(side=tk.RIGHT)
        
        # Bind escape key
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
    def overwrite(self):
        """Handle overwrite option"""
        self.result = "overwrite"
        self.dialog.destroy()
        
    def create_new(self):
        """Handle create new option"""
        self.result = "create_new"
        self.dialog.destroy()
        
    def cancel(self):
        """Handle cancel option"""
        self.result = "cancel"
        self.dialog.destroy()
        
    def get_result(self):
        """Get dialog result"""
        return self.result


class PasswordPopup:
    """Popup for displaying password"""
    
    def __init__(self, parent, controller, website, email, password):
        self.parent = parent
        self.controller = controller
        self.website = website
        self.email = email
        self.password = password
        
        self.create_popup()
        
    def create_popup(self):
        """Create password popup"""
        self.popup = tk.Toplevel(self.parent)
        self.popup.title(f"Password: {self.website}")
        self.popup.resizable(False, False)
        
        # Center popup
        self.popup.transient(self.parent)
        
        x = self.parent.winfo_rootx() + 100
        y = self.parent.winfo_rooty() + 100
        self.popup.geometry(f"+{x}+{y}")
        
        # Content frame
        content_frame = ttk.Frame(self.popup, padding=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Website
        ttk.Label(content_frame, text="Website:", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)
        ttk.Label(content_frame, text=self.website, font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(0, 10))
        
        # Email
        ttk.Label(content_frame, text="Email/Username:", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)
        ttk.Label(content_frame, text=self.email, font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(0, 10))
        
        # Password with show/hide
        password_frame = ttk.Frame(content_frame)
        password_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(password_frame, text="Password:", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        
        self.password_var = tk.StringVar(value="•" * 12)
        password_label = ttk.Label(password_frame, textvariable=self.password_var, font=("Consolas", 10))
        password_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Show/hide toggle
        self.show_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            password_frame,
            text="Show",
            variable=self.show_var,
            command=self.toggle_password,
            width=8
        ).pack(side=tk.RIGHT)
        
        # Buttons frame
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(
            button_frame,
            text="Copy Password",
            command=self.copy_password,
            style="Success.TButton",
            width=15
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="Copy Email",
            command=self.copy_email,
            style="Accent.TButton",
            width=15
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="Close",
            command=self.close,
            width=15
        ).pack(side=tk.RIGHT)
        
        # Bind escape key
        self.popup.bind('<Escape>', lambda e: self.close())
        self.popup.protocol("WM_DELETE_WINDOW", self.close)
        
    def toggle_password(self):
        """Toggle password visibility"""
        if self.show_var.get():
            self.password_var.set(self.password)
        else:
            self.password_var.set("•" * 12)
            
    def copy_password(self):
        """Copy password to clipboard"""
        pyperclip.copy(self.password)
        self.controller.show_popup_message("Password copied to clipboard!")
        
    def copy_email(self):
        """Copy email to clipboard"""
        pyperclip.copy(self.email)
        self.controller.show_popup_message("Email copied to clipboard!")
        
    def close(self):
        """Close the popup"""
        self.popup.destroy()