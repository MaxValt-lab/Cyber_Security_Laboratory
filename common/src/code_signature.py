"""
Digital Signature Module for Cyber_Security_Laboratory
Author: MaxValt-lab
Copyright (c) 2025
"""

import hashlib
import hmac
import time
import base64
from typing import Dict, Any
import json
import os

class CodeSignature:
    VERSION = "1.0.0"
    AUTHOR = "MaxValt-lab"
    PROJECT = "Cyber_Security_Laboratory"
    
    def __init__(self):
        self.timestamp = int(time.time())
        self.signature_key = os.urandom(32)
        
    def generate_file_signature(self, file_path: str) -> Dict[str, Any]:
        """Generate a unique signature for a file."""
        with open(file_path, 'rb') as f:
            content = f.read()
            
        # Создаем хеш файла
        file_hash = hashlib.sha256(content).hexdigest()
        
        # Создаем HMAC для аутентификации
        hmac_signature = hmac.new(
            self.signature_key,
            content,
            hashlib.sha256
        ).hexdigest()
        
        # Создаем временную метку
        timestamp = self.timestamp
        
        # Формируем сигнатуру
        signature = {
            "file": file_path,
            "author": self.AUTHOR,
            "project": self.PROJECT,
            "version": self.VERSION,
            "timestamp": timestamp,
            "hash": file_hash,
            "hmac": hmac_signature,
            "metadata": {
                "creation_date": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timestamp)),
                "copyright": f"© {time.strftime('%Y')} {self.AUTHOR}"
            }
        }
        
        return signature
    
    def verify_signature(self, file_path: str, signature: Dict[str, Any]) -> bool:
        """Verify file signature."""
        with open(file_path, 'rb') as f:
            content = f.read()
            
        current_hash = hashlib.sha256(content).hexdigest()
        
        return (
            current_hash == signature["hash"] and
            signature["author"] == self.AUTHOR and
            signature["project"] == self.PROJECT
        )
    
    def sign_project(self, project_root: str) -> Dict[str, Any]:
        """Sign entire project."""
        project_signature = {
            "project": self.PROJECT,
            "author": self.AUTHOR,
            "version": self.VERSION,
            "timestamp": self.timestamp,
            "files": {}
        }
        
        for root, _, files in os.walk(project_root):
            for file in files:
                if file.endswith(('.py', '.yml', '.json', '.md')):
                    file_path = os.path.join(root, file)
                    project_signature["files"][file_path] = self.generate_file_signature(file_path)
                    
        return project_signature

    def export_signature(self, signature: Dict[str, Any], output_file: str):
        """Export signature to file."""
        with open(output_file, 'w') as f:
            json.dump(signature, f, indent=2)
            
    def generate_proof_of_existence(self) -> str:
        """Generate proof of existence hash."""
        timestamp = str(self.timestamp).encode()
        project = self.PROJECT.encode()
        author = self.AUTHOR.encode()
        
        proof = hashlib.sha256(timestamp + project + author).hexdigest()
        return f"{self.AUTHOR}:{self.PROJECT}:{proof}"

if __name__ == "__main__":
    signer = CodeSignature()
    # Пример использования
    project_path = os.path.dirname(os.path.abspath(__file__))
    signature = signer.sign_project(project_path)
    signer.export_signature(signature, "project_signature.json")
    proof = signer.generate_proof_of_existence()
    print(f"Project signed successfully. Proof of existence: {proof}")