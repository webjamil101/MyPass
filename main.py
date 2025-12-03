#!/usr/bin/env python3
"""
Main entry point for the Password Manager application
"""
import tkinter as tk
from controllers.password_controller import PasswordController

def main():
    """Start the application"""
    root = tk.Tk()
    app = PasswordController(root)
    app.run()

if __name__ == "__main__":
    main()