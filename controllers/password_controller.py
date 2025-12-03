"""
Main controller for Password Manager
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.database import DatabaseManager
from models.security import SecurityManager
from views.main_window import MainWindow
from views.dialogs import DuplicateDialog, PasswordPopup
from utils.responsive import ResponsiveHelper
from styles.theme import apply_theme

logger = logging.getLogger(__name__)

class PasswordController:
    """Main controller coordinating models and views"""
    
    def __init__(self, root):
        self.root = root
        self.main_window = None  # Initialize as None
        
        # Initialize components
        self.setup_components()
        
        # Initialize UI
        self.setup_ui()
        
        logger.info("Password Manager initialized successfully")
    def load_initial_passwords(self):
        """Load passwords for initial display"""
        try:
            passwords = self.database.load_passwords()
            logger.info(f"Loaded {len(passwords)} passwords from database")
            return passwords
        except Exception as e:
            logger.error(f"Failed to load initial passwords: {e}")
            return []
   
    def setup_components(self):
        """Initialize model components"""
        try:
            # Initialize security
            self.security = SecurityManager()
            self.security.initialize()
            
            # Initialize database
            self.database = DatabaseManager()
            self.database.connect()
            
            # Initialize responsive helper
            self.responsive = ResponsiveHelper(self.root)
            self.responsive_vars = self.responsive.get_responsive_vars()
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            messagebox.showerror("Initialization Error", 
                                f"Failed to initialize application: {str(e)}")
            self.root.quit()
            
    def setup_ui(self):
        """Setup user interface"""
        try:
            # Apply theme
            apply_theme(self.root)
            
            # Create main window - pass self (controller) to it
            self.main_window = MainWindow(self.root, self, self.responsive_vars)
            
            # Bind window events
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.bind('<Configure>', self.on_window_resize)
            
            # Start responsive updates
            self.responsive.start_updates()
            
        except Exception as e:
            logger.error(f"Failed to setup UI: {e}")
            messagebox.showerror("UI Error", f"Failed to create user interface: {str(e)}")
            self.root.quit()
            
    def on_window_resize(self, event):
        """Handle window resize for responsive design"""
        if event.widget == self.root:
            # Update responsive variables
            self.responsive.update_responsive_vars()
            
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except Exception as e:
            logger.error(f"Application error: {e}")
            
    def on_closing(self):
        """Handle application closing"""
        try:
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                if self.database:
                    self.database.close()
                self.responsive.stop_updates()
                self.root.destroy()
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
            self.root.destroy()
    
    # Safe accessor methods that check if main_window exists
    def get_password_form(self):
        """Safely get password form instance"""
        if self.main_window:
            return self.main_window.get_password_form()
        return None
    
    def get_password_list(self):
        """Safely get password list instance"""
        if self.main_window:
            return self.main_window.get_password_list()
        return None
    
    def update_status(self, message: str):
        """Safely update status bar"""
        if self.main_window:
            self.main_window.update_status(message)
    
    # New methods for advanced functionality
    def generate_advanced_password(self, **kwargs):
        """Generate password with advanced options"""
        return self.security.generate_advanced_password(**kwargs)
    
    def get_default_symbols(self):
        """Get default symbols"""
        return self.security.get_default_symbols()
    
    def get_default_numbers(self):
        """Get default numbers"""
        return self.security.get_default_numbers()
    
    def filter_passwords(self, search_term):
        """Filter passwords"""
        try:
            password_list = self.get_password_list()
            if password_list and search_term:
                results = self.database.search_passwords(search_term)
                password_list.filter_list(results)
                self.update_status(f"Filtered to {len(results)} passwords")
            else:
                self.refresh_password_list()
        except Exception as e:
            logger.error(f"Failed to filter passwords: {e}")
            self.show_popup_message(f"Error filtering passwords: {str(e)}", is_error=True)
    
    def auto_fill_form(self, website):
        """Auto-fill form with data from selected password"""
        try:
            # Get password details from database
            passwords = self.database.load_passwords()
            for pw in passwords:
                pw_website, category, email, encrypted_password, date_added = pw
                if pw_website == website:
                    # Decrypt password
                    password = self.security.decrypt_data(encrypted_password)
                    
                    # Update form fields
                    form = self.get_password_form()
                    if form:
                        form.website_entry.delete(0, tk.END)
                        form.website_entry.insert(0, website)
                        
                        form.email_entry.set_text(email)
                        
                        form.password_entry.delete(0, tk.END)
                        form.password_entry.insert(0, password)
                        
                        form.category_var.set(category)
                        
                        self.show_popup_message(f"Form auto-filled for {website}")
                    return
                    
            self.show_popup_message(f"No password found for {website}", is_error=True)
            
        except Exception as e:
            logger.error(f"Failed to auto-fill form: {e}")
            self.show_popup_message(f"Error auto-filling form: {str(e)}", is_error=True)
    
    # Enhanced methods
    def save_password(self, website, email, password, category):
        """Save a password with enhanced duplicate handling"""
        try:
            # Validate inputs
            if not website.strip():
                return False, "Website is required"
            if not email.strip():
                return False, "Email/Username is required"
            if not password.strip():
                return False, "Password is required"
                
            # Check for duplicates
            exact_match, duplicates = self.database.check_duplicate(website, email)
            
            if exact_match:
                # Show duplicate dialog
                dialog = DuplicateDialog(self.root, self, (exact_match, duplicates))
                self.root.wait_window(dialog.dialog)
                
                result = dialog.get_result()
                
                if result == "cancel":
                    return False, "Operation cancelled"
                elif result == "create_new":
                    website = self.database.get_unique_website_name(website)
                    # Fall through to save
                elif result == "overwrite":
                    # Proceed with overwrite
                    pass
                    
            # Encrypt and save password
            encrypted_password = self.security.encrypt_data(password)
            password_hash, salt = self.security.hash_password(password)
            
            success = self.database.save_password(
                website=website,
                email=email,
                encrypted_password=encrypted_password,
                salt=salt,
                category=category
            )
            
            if success:
                message = f"Password saved for {website}"
                if exact_match and result == "overwrite":
                    message = f"Password updated for {website}"
                return True, message
            else:
                return False, f"Failed to save password for {website}"
                
        except Exception as e:
            logger.error(f"Failed to save password: {e}")
            return False, f"Error: {str(e)}"
    
    def search_passwords(self, search_term):
        """Search passwords"""
        try:
            if search_term:
                results = self.database.search_passwords(search_term)
                password_list = self.get_password_list()
                if password_list:
                    password_list.update_list(results)
                self.update_status(f"Found {len(results)} results for '{search_term}'")
            else:
                self.refresh_password_list()
        except Exception as e:
            logger.error(f"Failed to search passwords: {e}")
            self.show_popup_message(f"Error searching passwords: {str(e)}", is_error=True)
            
    def refresh_password_list(self):
        """Refresh password list"""
        try:
            passwords = self.database.load_passwords()
            password_list = self.get_password_list()
            if password_list:
                password_list.update_list(passwords)
            self.update_status(f"Showing {len(passwords)} passwords")
        except Exception as e:
            logger.error(f"Failed to refresh password list: {e}")
            self.show_popup_message(f"Error loading passwords: {str(e)}", is_error=True)
            
    def delete_password(self, website, email):
        """Delete a password"""
        try:
            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete the password for {website}?"
            )
            
            if confirm:
                success = self.database.delete_password(website, email)
                if success:
                    self.show_popup_message(f"Password deleted for {website}")
                    self.refresh_password_list()
                else:
                    self.show_popup_message(f"Failed to delete password for {website}", is_error=True)
                    
        except Exception as e:
            logger.error(f"Failed to delete password: {e}")
            self.show_popup_message(f"Error deleting password: {str(e)}", is_error=True)
            
    def show_password_popup(self, website, email, encrypted_password):
        """Show password in popup"""
        try:
            password = self.decrypt_password(encrypted_password)
            PasswordPopup(self.root, self, website, email, password)
        except Exception as e:
            logger.error(f"Failed to show password: {e}")
            self.show_popup_message(f"Error showing password: {str(e)}", is_error=True)
            
    def decrypt_password(self, encrypted_password):
        """Decrypt a password"""
        return self.security.decrypt_data(encrypted_password)
        
    def check_password_strength(self, password):
        """Check password strength"""
        return self.security.check_password_strength(password)
        
    def show_popup_message(self, message, is_error=False):
        """Show a popup message"""
        self.update_status(message)
        if is_error:
            messagebox.showerror("Error", message)
        else:
            messagebox.showinfo("Info", message)