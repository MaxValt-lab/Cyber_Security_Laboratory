"""
Core security utilities for the Cyber Security Laboratory.
"""

import hashlib
import base64
import os
from typing import Optional, Dict, Any

class SecurityUtils:
    @staticmethod
    def generate_secure_hash(data: str, salt: Optional[str] = None) -> Dict[str, str]:
        """Generate a secure hash using SHA-256."""
        if not salt:
            salt = base64.b64encode(os.urandom(32)).decode('utf-8')
        
        # Combine data and salt
        salted_data = f"{data}{salt}"
        
        # Generate hash
        hash_obj = hashlib.sha256(salted_data.encode())
        hash_value = hash_obj.hexdigest()
        
        return {
            "hash": hash_value,
            "salt": salt
        }
    
    @staticmethod
    def verify_hash(data: str, hash_value: str, salt: str) -> bool:
        """Verify a hash against the original data."""
        new_hash = SecurityUtils.generate_secure_hash(data, salt)["hash"]
        return new_hash == hash_value

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Generate a secure random token."""
        return base64.b64encode(os.urandom(length)).decode('utf-8')