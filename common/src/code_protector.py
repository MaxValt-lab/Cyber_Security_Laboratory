"""
Advanced Code Protection System for Cyber_Security_Laboratory
Author: MaxValt-lab
Copyright (c) 2025
"""

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Dict, Any
import platform
import uuid
import json

class CodeProtector:
    def __init__(self):
        self._hardware_id = self._generate_hardware_id()
        self._encryption_key = self._generate_key()
        self._fernet = Fernet(self._encryption_key)
        self._protected_sections: Dict[str, str] = {}
        
    def _generate_hardware_id(self) -> str:
        """Генерирует уникальный идентификатор оборудования."""
        system_info = {
            'platform': platform.system(),
            'processor': platform.processor(),
            'machine': platform.machine(),
            'node': platform.node(),
            'mac_address': uuid.getnode()
        }
        return str(hash(frozenset(system_info.items())))
        
    def _generate_key(self) -> bytes:
        """Генерирует ключ шифрования на основе hardware_id."""
        salt = b'MaxValt_Lab_Salt'  # Уникальная соль для проекта
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self._hardware_id.encode()))
        return key
        
    def protect_code_section(self, section_name: str, code: str) -> str:
        """Шифрует секцию кода."""
        encrypted = self._fernet.encrypt(code.encode())
        self._protected_sections[section_name] = encrypted.decode()
        
        # Генерируем код для расшифровки
        decoder = f'''
def _decode_{section_name}():
    import base64
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import platform
    import uuid

    def _get_hardware_id():
        system_info = {{
            'platform': platform.system(),
            'processor': platform.processor(),
            'machine': platform.machine(),
            'node': platform.node(),
            'mac_address': uuid.getnode()
        }}
        return str(hash(frozenset(system_info.items())))

    def _get_key():
        salt = b'MaxValt_Lab_Salt'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(_get_hardware_id().encode()))
        return key

    encrypted = '{encrypted.decode()}'
    f = Fernet(_get_key())
    code = f.decrypt(encrypted.encode()).decode()
    return code

# Выполняем защищенный код
exec(_decode_{section_name}())
'''
        return decoder
        
    def export_protected_sections(self, output_path: str) -> None:
        """Экспортирует защищенные секции в файл."""
        with open(output_path, 'w') as f:
            json.dump({
                'hardware_id': self._hardware_id,
                'sections': self._protected_sections
            }, f, indent=2)

    @staticmethod
    def verify_hardware(stored_id: str) -> bool:
        """Проверяет, совпадает ли текущее оборудование с сохраненным."""
        current_protector = CodeProtector()
        return stored_id == current_protector._hardware_id