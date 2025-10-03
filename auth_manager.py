import hashlib
import os
import base64
from datetime import datetime
from passlib.hash import scrypt, pbkdf2_sha256
from config import Config

class AuthManager:
    @staticmethod
    def generate_salt(length=32):
        """Generate a cryptographically secure random salt"""
        return os.urandom(length)
    
    @staticmethod
    def hash_with_scrypt(password, salt=None):
        """Hash password using scrypt algorithm"""
        if salt is None:
            salt = AuthManager.generate_salt()
        
        # Using passlib's scrypt implementation with correct parameter names
        hashed = scrypt.using(
            rounds=Config.SCRYPT_N,  # CPU/memory cost parameter (N)
            block_size=Config.SCRYPT_R,  # Block size parameter (r)
            parallelism=Config.SCRYPT_P,  # Parallelization parameter (p)
            salt_size=32
        ).hash(password)
        
        return hashed
    
    @staticmethod
    def hash_with_pbkdf2(password, salt=None):
        """Hash password using PBKDF2-HMAC-SHA256"""
        if salt is None:
            salt = AuthManager.generate_salt()
        
        # Using passlib's PBKDF2 implementation
        hashed = pbkdf2_sha256.using(
            rounds=Config.PBKDF2_ROUNDS,
            salt_size=32
        ).hash(password)
        
        return hashed
    
    @staticmethod
    def verify_scrypt(password, hashed):
        """Verify password against scrypt hash"""
        return scrypt.verify(password, hashed)
    
    @staticmethod
    def verify_pbkdf2(password, hashed):
        """Verify password against PBKDF2 hash"""
        return pbkdf2_sha256.verify(password, hashed)
    
    @staticmethod
    def create_user_data(email, password, algorithm='scrypt'):
        """Create user data with hashed password"""
        if algorithm == 'scrypt':
            hashed_password = AuthManager.hash_with_scrypt(password)
        elif algorithm == 'pbkdf2':
            hashed_password = AuthManager.hash_with_pbkdf2(password)
        else:
            raise ValueError("Unsupported algorithm")
        
        return {
            "email": email,
            "password": hashed_password,
            "algorithm": algorithm,
            "created_at": datetime.utcnow()
        }