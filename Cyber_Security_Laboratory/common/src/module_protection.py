"""
Module Protection System for Cyber_Security_Laboratory
Author: MaxValt-lab
Copyright (c) 2025

This module implements protection against:
- Unauthorized code copying
- Module separation
- Code extraction
"""

import hashlib
import os
import sys
import uuid
import time
import json
from typing import Dict, Any, Optional
from pathlib import Path

class ModuleProtection:
    def __init__(self):
        self._module_id = str(uuid.uuid4())
        self._initialization_time = time.time()
        self._module_registry: Dict[str, Any] = {}
        self._integrity_keys: Dict[str, str] = {}
        self._module_dependencies: Dict[str, set] = {}
        
    @property
    def module_id(self) -> str:
        return self._module_id
        
    def _calculate_module_hash(self, module_path: str) -> str:
        """Calculate cryptographic hash of module contents."""
        with open(module_path, 'rb') as f:
            content = f.read()
        return hashlib.sha256(content).hexdigest()
    
    def _verify_module_location(self, module_path: str) -> bool:
        """Verify that module is in its original location."""
        try:
            expected_path = self._module_registry[Path(module_path).name]['original_path']
            return os.path.abspath(module_path) == os.path.abspath(expected_path)
        except KeyError:
            return False
            
    def _check_module_integrity(self, module_path: str) -> bool:
        """Verify module integrity."""
        try:
            current_hash = self._calculate_module_hash(module_path)
            original_hash = self._module_registry[Path(module_path).name]['hash']
            return current_hash == original_hash
        except (KeyError, FileNotFoundError):
            return False
            
    def register_module(self, module_path: str, dependencies: Optional[list] = None) -> None:
        """Register a module with the protection system."""
        module_name = Path(module_path).name
        
        # Создаем уникальный ключ для модуля
        module_key = hashlib.sha256(
            f"{self._module_id}:{module_name}:{time.time()}".encode()
        ).hexdigest()
        
        self._module_registry[module_name] = {
            'hash': self._calculate_module_hash(module_path),
            'original_path': os.path.abspath(module_path),
            'registration_time': time.time(),
            'key': module_key
        }
        
        # Регистрируем зависимости
        if dependencies:
            self._module_dependencies[module_name] = set(dependencies)
            
        # Встраиваем защитный код в модуль
        self._inject_protection(module_path, module_key)
    
    def _inject_protection(self, module_path: str, module_key: str) -> None:
        """Встраивает защитный код в модуль."""
        with open(module_path, 'r') as f:
            content = f.read()
            
        protection_code = f'''
# === BEGIN PROTECTION CODE ===
import os
import hashlib
import time

def _verify_module_integrity():
    module_key = "{module_key}"
    module_path = __file__
    
    # Проверка оригинального расположения
    if not os.path.abspath(module_path) == "{os.path.abspath(module_path)}":
        raise RuntimeError("Module location verification failed")
        
    # Проверка целостности кода
    with open(module_path, 'rb') as f:
        content = f.read()
    current_hash = hashlib.sha256(content).hexdigest()
    if current_hash != "{self._calculate_module_hash(module_path)}":
        raise RuntimeError("Module integrity check failed")
        
    # Проверка времени
    if time.time() - {self._initialization_time} > 86400:  # 24 часа
        raise RuntimeError("Module time check failed")

_verify_module_integrity()
# === END PROTECTION CODE ===

'''
        
        # Добавляем защитный код в начало файла
        with open(module_path, 'w') as f:
            f.write(protection_code + content)
            
    def verify_all_modules(self) -> bool:
        """Проверить целостность всех зарегистрированных модулей."""
        for module_name, module_info in self._module_registry.items():
            if not self._verify_module_location(module_info['original_path']):
                raise RuntimeError(f"Module location verification failed: {module_name}")
                
            if not self._check_module_integrity(module_info['original_path']):
                raise RuntimeError(f"Module integrity check failed: {module_name}")
                
            # Проверяем зависимости
            if module_name in self._module_dependencies:
                for dep in self._module_dependencies[module_name]:
                    if dep not in self._module_registry:
                        raise RuntimeError(f"Missing dependency {dep} for module {module_name}")
        
        return True
        
    def create_module_manifest(self, output_path: str) -> None:
        """Создать манифест модулей с информацией о зависимостях."""
        manifest = {
            'system_id': self._module_id,
            'creation_time': self._initialization_time,
            'modules': self._module_registry,
            'dependencies': {k: list(v) for k, v in self._module_dependencies.items()}
        }
        
        with open(output_path, 'w') as f:
            json.dump(manifest, f, indent=2)
            
# Создаем глобальный экземпляр защиты
protection_system = ModuleProtection()