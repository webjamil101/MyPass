"""
Database management for Password Manager
"""
import sqlite3
from datetime import datetime
from typing import List, Tuple, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Handles all database operations for the Password Manager"""
    
    def __init__(self, db_path: str = 'passwords.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Connect to the database"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self._initialize_database()
            logger.info("Database connected successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def _initialize_database(self):
        """Initialize database with required tables"""
        # Create passwords table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                email TEXT NOT NULL,
                encrypted_password TEXT NOT NULL,
                salt TEXT NOT NULL,
                date_added TEXT NOT NULL,
                category TEXT DEFAULT 'General',
                UNIQUE(website, email)
            )
        ''')
        
        self.conn.commit()
    
    def diagnose_database(self) -> bool:
        """Diagnose database issues"""
        try:
            logger.info("Database diagnosis started")
            
            # Check if table exists
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='passwords'")
            table_exists = self.cursor.fetchone()
            
            if not table_exists:
                logger.error("Table 'passwords' does not exist")
                return False
            
            # Check columns
            self.cursor.execute("PRAGMA table_info(passwords)")
            columns = self.cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            required_columns = ['website', 'email', 'encrypted_password', 'salt', 'date_added', 'category']
            missing_columns = [col for col in required_columns if col not in column_names]
            
            if missing_columns:
                logger.error(f"Missing columns: {missing_columns}")
                return False
            
            logger.info("Database diagnosis passed")
            return True
            
        except Exception as e:
            logger.error(f"Database diagnosis failed: {e}")
            return False
    
    def save_password(self, website: str, email: str, encrypted_password: str, 
                     salt: str, category: str = "General") -> bool:
        """Save password to database"""
        try:
            current_time = datetime.now().isoformat()
            
            # Check if entry exists
            self.cursor.execute('SELECT website FROM passwords WHERE website = ? AND email = ?', 
                              (website, email))
            existing = self.cursor.fetchone()
            
            if existing:
                # Update existing entry
                self.cursor.execute('''
                    UPDATE passwords 
                    SET encrypted_password = ?, salt = ?, date_added = ?, category = ?
                    WHERE website = ? AND email = ?
                ''', (encrypted_password, salt, current_time, category, website, email))
            else:
                # Insert new entry
                self.cursor.execute('''
                    INSERT INTO passwords (website, email, encrypted_password, salt, date_added, category)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (website, email, encrypted_password, salt, current_time, category))
            
            self.conn.commit()
            logger.info(f"Password saved for {website}")
            return True
            
        except sqlite3.IntegrityError as e:
            logger.error(f"Duplicate entry for {website}: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to save password for {website}: {e}")
            return False
    
    def load_passwords(self) -> List[Tuple]:
        """Load all passwords from database"""
        try:
            self.cursor.execute('''
                SELECT website, category, email, encrypted_password, date_added 
                FROM passwords ORDER BY website
            ''')
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Failed to load passwords: {e}")
            return []
    
    def search_passwords(self, search_term: str) -> List[Tuple]:
        """Search passwords by website name"""
        try:
            self.cursor.execute('''
                SELECT website, category, email, encrypted_password, date_added 
                FROM passwords WHERE website LIKE ?
            ''', (f'%{search_term}%',))
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Failed to search passwords: {e}")
            return []
    
    def delete_password(self, website: str, email: str) -> bool:
        """Delete password from database"""
        try:
            self.cursor.execute('DELETE FROM passwords WHERE website = ? AND email = ?', 
                              (website, email))
            self.conn.commit()
            logger.info(f"Password deleted for {website}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete password for {website}: {e}")
            return False
    
    def check_duplicate(self, website: str, email: str) -> Tuple[Optional[Dict], List[Dict]]:
        """Check for duplicate entries"""
        try:
            self.cursor.execute('''
                SELECT website, email, category, date_added 
                FROM passwords 
                WHERE website LIKE ? OR email LIKE ?
            ''', (f'%{website}%', f'%{email}%'))
            
            results = self.cursor.fetchall()
            
            duplicates = []
            exact_match = None
            
            for result in results:
                result_website, result_email, result_category, result_date = result
                if result_website.lower() == website.lower() and result_email.lower() == email.lower():
                    exact_match = {
                        'website': result_website,
                        'email': result_email,
                        'category': result_category,
                        'date_added': result_date
                    }
                else:
                    duplicates.append({
                        'website': result_website,
                        'email': result_email,
                        'category': result_category,
                        'date_added': result_date
                    })
            
            return exact_match, duplicates
            
        except Exception as e:
            logger.error(f"Error checking duplicates: {e}")
            return None, []
    
    def get_unique_website_name(self, base_name: str) -> str:
        """Generate a unique website name by appending a number"""
        counter = 1
        new_name = f"{base_name} ({counter})"
        
        while True:
            self.cursor.execute('SELECT COUNT(*) FROM passwords WHERE website = ?', (new_name,))
            if self.cursor.fetchone()[0] == 0:
                return new_name
            counter += 1
            new_name = f"{base_name} ({counter})"
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")