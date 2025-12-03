"""
Security and encryption management for Password Manager
"""
import os
import hashlib
import secrets
import base64
from cryptography.fernet import Fernet
from typing import Tuple
import logging
from random import choice, shuffle

logger = logging.getLogger(__name__)

class SecurityManager:
    """Handles all security and encryption operations"""
    
    def __init__(self, key_file: str = "master.key"):
        self.key_file = key_file
        self.cipher_suite = None
        self.default_symbols = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        
    def initialize(self):
        """Initialize encryption system"""
        try:
            # Generate or load encryption key
            if not os.path.exists(self.key_file):
                key = Fernet.generate_key()
                with open(self.key_file, "wb") as key_file:
                    key_file.write(key)
                logger.info("New encryption key generated")
            
            with open(self.key_file, "rb") as key_file:
                key = key_file.read()
            
            self.cipher_suite = Fernet(key)
            logger.info("Security system initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize security: {e}")
            raise
    
    def hash_password(self, password: str) -> Tuple[str, str]:
        """Hash password with salt using PBKDF2"""
        try:
            salt = secrets.token_bytes(32)
            password_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt,
                100000  # 100,000 iterations
            )
            return base64.b64encode(password_hash).decode('utf-8'), base64.b64encode(salt).decode('utf-8')
        except Exception as e:
            logger.error(f"Failed to hash password: {e}")
            raise
    
    def verify_password(self, password: str, stored_hash: str, salt: str) -> bool:
        """Verify password against stored hash"""
        try:
            salt_bytes = base64.b64decode(salt)
            password_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt_bytes,
                100000
            )
            return base64.b64encode(password_hash).decode('utf-8') == stored_hash
        except Exception as e:
            logger.error(f"Failed to verify password: {e}")
            return False
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt data using Fernet symmetric encryption"""
        try:
            if not self.cipher_suite:
                raise ValueError("Security manager not initialized")
            return self.cipher_suite.encrypt(data.encode()).decode()
        except Exception as e:
            logger.error(f"Failed to encrypt data: {e}")
            raise
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt data using Fernet symmetric encryption"""
        try:
            if not self.cipher_suite:
                raise ValueError("Security manager not initialized")
            return self.cipher_suite.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            logger.error(f"Failed to decrypt data: {e}")
            raise
    
    def check_password_strength(self, password: str) -> Tuple[str, str, int]:
        """Analyze password strength and return level, color, and score"""
        score = 0
        
        # Length checks
        if len(password) >= 8: score += 1
        if len(password) >= 12: score += 1
        if len(password) >= 16: score += 1
        
        # Character variety checks
        if any(c.islower() for c in password): score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password): score += 1
        
        # Determine strength level
        strength_levels = {
            0: ("Very Weak", "#f44336"),
            1: ("Very Weak", "#f44336"),
            2: ("Weak", "#FF9800"),
            3: ("Fair", "#FFC107"),
            4: ("Good", "#8BC34A"),
            5: ("Strong", "#4CAF50"),
            6: ("Very Strong", "#2E7D32"),
            7: ("Excellent", "#1B5E20")
        }
        
        level, color = strength_levels.get(score, ("Unknown", "#757575"))
        return level, color, score
    
    def generate_advanced_password(self, length: int = 16, use_lowercase: bool = True, 
                                 use_uppercase: bool = True, use_numbers: bool = True, 
                                 use_symbols: bool = True, custom_symbols: str = None,
                                 custom_numbers: str = None) -> str:
        """Generate a secure password with customizable options"""
        try:
            # Use defaults if not provided
            if custom_symbols is None:
                custom_symbols = self.default_symbols
            if custom_numbers is None:
                custom_numbers = '0123456789'
            
            # Validate length
            if length < 8 or length > 50:
                raise ValueError("Password length must be between 8 and 50 characters")
            
            # Get character sets based on user selections
            lowercase = 'abcdefghijklmnopqrstuvwxyz' if use_lowercase else ''
            uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if use_uppercase else ''
            numbers = custom_numbers if use_numbers else ''
            symbols = custom_symbols if use_symbols else ''
            
            # Build character set
            chars = lowercase + uppercase + numbers + symbols
            
            if not chars:
                raise ValueError("Please select at least one character type")
            
            # Ensure password meets basic requirements
            password_parts = []
            
            if use_lowercase and lowercase:
                password_parts.append(choice(lowercase))
            if use_uppercase and uppercase:
                password_parts.append(choice(uppercase))
            if use_numbers and numbers:
                password_parts.append(choice(numbers))
            if use_symbols and symbols:
                password_parts.append(choice(symbols))
            
            # Fill remaining length
            remaining_length = max(0, length - len(password_parts))
            if remaining_length > 0:
                password_parts += [choice(chars) for _ in range(remaining_length)]
            
            # Shuffle to randomize order
            shuffle(password_parts)
            
            return ''.join(password_parts)
            
        except Exception as e:
            logger.error(f"Failed to generate password: {e}")
            raise
    
    def get_default_symbols(self) -> str:
        """Get default symbols"""
        return self.default_symbols
    
    def get_default_numbers(self) -> str:
        """Get default numbers"""
        return '0123456789'