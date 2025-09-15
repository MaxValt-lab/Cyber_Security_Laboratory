"""
Module Initialization System for Cyber_Security_Laboratory
Author: MaxValt-lab
Copyright (c) 2025
"""

import os
from pathlib import Path
from typing import List, Optional
from .module_protection import protection_system

class ModuleInitializer:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        
    def _find_python_files(self, directory: Path) -> List[Path]:
        """Рекурсивно находит все Python файлы в директории."""
        python_files = []
        for item in directory.rglob("*.py"):
            if "venv" not in str(item) and "test" not in str(item):
                python_files.append(item)
        return python_files
        
    def _analyze_dependencies(self, file_path: Path) -> List[str]:
        """Анализирует зависимости модуля."""
        dependencies = []
        with open(file_path, 'r') as f:
            content = f.readlines()
            
        for line in content:
            if line.startswith('from') or line.startswith('import'):
                # Извлекаем имя модуля
                module_name = line.split()[1].split('.')[0]
                if module_name not in ['os', 'sys', 'typing', 'pathlib']:
                    dependencies.append(module_name)
                    
        return dependencies
        
    def initialize_all_modules(self):
        """Инициализирует защиту для всех модулей проекта."""
        python_files = self._find_python_files(self.project_root)
        
        # Сначала анализируем зависимости
        dependencies_map = {}
        for file_path in python_files:
            deps = self._analyze_dependencies(file_path)
            dependencies_map[file_path.name] = deps
            
        # Регистрируем модули
        for file_path in python_files:
            protection_system.register_module(
                str(file_path),
                dependencies_map[file_path.name]
            )
            
        # Создаем манифест
        manifest_path = self.project_root / 'module_manifest.json'
        protection_system.create_module_manifest(str(manifest_path))
        
        return len(python_files)

def initialize_protection():
    """Функция для инициализации защиты всех модулей."""
    initializer = ModuleInitializer()
    modules_count = initializer.initialize_all_modules()
    print(f"Protected {modules_count} modules")