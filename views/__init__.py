"""
Views package for Password Manager
"""
from .main_window import MainWindow
from .password_form import PasswordForm
from .password_list import PasswordList
from .dialogs import DuplicateDialog, PasswordPopup

__all__ = ['MainWindow', 'PasswordForm', 'PasswordList', 'DuplicateDialog', 'PasswordPopup']