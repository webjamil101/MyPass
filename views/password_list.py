"""
Password list view for Password Manager
"""
import tkinter as tk
from tkinter import ttk
import pyperclip
import logging
from .dialogs import PasswordPopup
from datetime import datetime

logger = logging.getLogger(__name__)

class PasswordList:
    """Password list view"""
    
    def __init__(self, parent, controller, responsive_vars, compact=False):
        self.parent = parent
        self.controller = controller
        self.responsive_vars = responsive_vars
        self.compact = compact
        self.all_passwords = []  # Store all passwords for filtering
        
        self.create_list()
        self.load_initial_passwords()
        self.controller.refresh_password_list()
    def load_initial_passwords(self):
        """Load passwords immediately after creation"""
        try:
            # Call controller to load passwords
            passwords = self.controller.load_initial_passwords()
            if passwords:
                self.update_list(passwords)
        except Exception as e:
            logger.error(f"Failed to load initial passwords: {e}")
    def create_list(self):
        """Create password list view"""
        # Search frame
        search_frame = ttk.Frame(self.parent)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Filter:").pack(side=tk.LEFT, padx=(0, 8))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        # Clear filter button
        clear_width = 10 if self.compact else 12
        ttk.Button(
            search_frame,
            text="Clear Filter",
            command=self.clear_filter,
            width=clear_width
        ).pack(side=tk.RIGHT, padx=(8, 0))
        
        # Treeview frame
        tree_frame = ttk.Frame(self.parent)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview columns based on screen size
        if self.compact:
            columns = ('Website', 'Category')
            column_widths = {'Website': 120, 'Category': 80}
        else:
            columns = ('Website', 'Category', 'Email', 'Date Added')
            column_widths = {'Website': 150, 'Category': 100, 'Email': 180, 'Date Added': 120}
        
        # Create Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            selectmode='browse',
            height=10 if self.compact else 15
        )
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[col], minwidth=50)
        
        # Bind events
        self.tree.bind('<Double-Button-1>', self.on_item_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu)
        
        # Pack tree and scrollbars
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Context menu
        self.context_menu = tk.Menu(self.parent, tearoff=0)
        self.context_menu.add_command(label="Show Password", command=self.show_selected_password)
        self.context_menu.add_command(label="Copy Password", command=self.copy_selected_password)
        self.context_menu.add_command(label="Auto-Fill Form", command=self.auto_fill_from_selection)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Delete", command=self.delete_selected_password)
        
        # Action buttons with responsive layout
        self.create_action_buttons()
        
    def create_action_buttons(self):
        """Create action buttons"""
        action_frame = ttk.Frame(self.parent)
        action_frame.pack(fill=tk.X, pady=(8, 0))
        
        action_button_width = 12 if self.compact else 15
        
        if self.compact:
            # Stack buttons vertically for small screens
            row1 = ttk.Frame(action_frame)
            row1.pack(fill=tk.X, pady=2)
            
            ttk.Button(
                row1, 
                text="Copy Password", 
                command=self.copy_selected_password,
                width=action_button_width
            ).pack(side=tk.LEFT, padx=(0, 5))
            
            ttk.Button(
                row1, 
                text="Show Password", 
                command=self.show_selected_password,
                width=action_button_width
            ).pack(side=tk.LEFT, padx=(0, 5))
            
            row2 = ttk.Frame(action_frame)
            row2.pack(fill=tk.X, pady=2)
            
            ttk.Button(
                row2, 
                text="Auto-Fill Form", 
                command=self.auto_fill_from_selection,
                width=action_button_width
            ).pack(side=tk.LEFT, padx=(0, 5))
            
            ttk.Button(
                row2, 
                text="Delete", 
                command=self.delete_selected_password,
                style="Danger.TButton",
                width=action_button_width
            ).pack(side=tk.RIGHT)
        else:
            # Horizontal layout for larger screens
            ttk.Button(
                action_frame, 
                text="Copy Password", 
                command=self.copy_selected_password,
                width=action_button_width
            ).pack(side=tk.LEFT, padx=(0, 8))
            
            ttk.Button(
                action_frame, 
                text="Show Password", 
                command=self.show_selected_password,
                width=action_button_width
            ).pack(side=tk.LEFT, padx=(0, 8))
            
            ttk.Button(
                action_frame, 
                text="Auto-Fill Form", 
                command=self.auto_fill_from_selection,
                width=action_button_width
            ).pack(side=tk.LEFT, padx=(0, 8))
            
            ttk.Button(
                action_frame, 
                text="Delete", 
                command=self.delete_selected_password,
                style="Danger.TButton",
                width=action_button_width
            ).pack(side=tk.RIGHT)
    
    def on_search(self, event=None):
        """Handle search/filter"""
        search_term = self.search_var.get().lower()
        self.filter_list(self.all_passwords, search_term)
        
    def filter_list(self, passwords, search_term=""):
        """Filter the password list"""
        if not search_term:
            self.update_list(passwords)
            return
            
        filtered = []
        for pw in passwords:
            website, category, email, encrypted_password, date_added = pw
            if (search_term in website.lower() or 
                search_term in category.lower() or 
                search_term in email.lower()):
                filtered.append(pw)
        
        self.update_list(filtered)
        
    def clear_filter(self):
        """Clear filter and show all passwords"""
        self.search_var.set("")
        self.update_list(self.all_passwords)
        
    def update_list(self, passwords):
        """Update the password list"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Store all passwords for filtering
        self.all_passwords = passwords
            
        # Insert new items
        for pw in passwords:
            website, category, email, encrypted_password, date_added = pw
            
            if self.compact:
                # Truncate values for compact view
                display_email = email[:15] + '...' if len(email) > 15 else email
                values = (website, category)
            else:
                # Format date for display
                formatted_date = self.format_date(date_added)
                values = (website, category, email, formatted_date)
                
            self.tree.insert('', 'end', values=values, text='', 
                           tags=(website, email, encrypted_password))
            
    def format_date(self, date_string):
        """Format date for display"""
        try:
            dt = datetime.fromisoformat(date_string)
            return dt.strftime("%Y-%m-%d")
        except:
            return date_string
            
    def on_item_double_click(self, event):
        """Handle double-click on item"""
        self.show_selected_password()
        
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        try:
            item = self.tree.identify_row(event.y)
            if item:
                self.tree.selection_set(item)
                self.context_menu.post(event.x_root, event.y_root)
        except:
            pass
            
    def show_selected_password(self):
        """Show password for selected item"""
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            website = self.tree.item(item, 'tags')[0]
            email = self.tree.item(item, 'tags')[1]
            encrypted_password = self.tree.item(item, 'tags')[2]
            self.controller.show_password_popup(website, email, encrypted_password)
            
    def copy_selected_password(self):
        """Copy password to clipboard"""
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            website = self.tree.item(item, 'tags')[0]
            email = self.tree.item(item, 'tags')[1]
            encrypted_password = self.tree.item(item, 'tags')[2]
            
            try:
                password = self.controller.decrypt_password(encrypted_password)
                pyperclip.copy(password)
                self.controller.show_popup_message(f"Password for {website} copied to clipboard!")
            except Exception as e:
                logger.error(f"Failed to copy password: {e}")
                self.controller.show_popup_message(f"Error copying password: {str(e)}", is_error=True)
                
    def auto_fill_from_selection(self):
        """Auto-fill form from selected item"""
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            website = self.tree.item(item, 'tags')[0]
            self.controller.auto_fill_form(website)
                
    def delete_selected_password(self):
        """Delete selected password"""
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            website = self.tree.item(item, 'tags')[0]
            email = self.tree.item(item, 'tags')[1]
            self.controller.delete_password(website, email)