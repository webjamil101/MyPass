"""
Input validators for Password Manager
"""
import re

def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email string to validate
        
    Returns:
        bool: True if valid email format
    """
    if not email:
        return False
        
    # Simple email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> tuple:
    """
    Validate password strength
    
    Args:
        password: Password string to validate
        
    Returns:
        tuple: (is_valid, error_messages)
    """
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one number")
    
    # Check for special characters
    special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
    if not any(c in special_chars for c in password):
        errors.append("Password must contain at least one special character")
    
    return len(errors) == 0, errors

def validate_website(url: str) -> bool:
    """
    Validate website URL format
    
    Args:
        url: Website URL string to validate
        
    Returns:
        bool: True if valid website format
    """
    if not url:
        return False
    
    # Remove protocol and www for validation
    clean_url = url.lower()
    clean_url = re.sub(r'^https?://', '', clean_url)
    clean_url = re.sub(r'^www\.', '', clean_url)
    
    # Check for at least one dot and valid characters
    if '.' not in clean_url:
        return False
    
    # Check for valid characters
    pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, clean_url))