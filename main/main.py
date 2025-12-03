#!/usr/bin/env python3
"""
Main entry point for the Password Manager application
"""
import sys
import os
import tkinter as tk

# Add the project root to Python path to enable imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from controllers.password_controller import PasswordController

def main():
    """Start the application"""
    root = tk.Tk()
    app = PasswordController(root)
    app.run()

if __name__ == "__main__":
    main()