#!/usr/bin/env python3
import os
import re
import json
from pathlib import Path

class AutoFixerAgent:
    def __init__(self):
        self.fixes_applied = []
        
    def fix_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            fixes = []
            
            # Исправление пробелов
            if re.search(r' +\n', content):
                content = re.sub(r' +\n', '\n', content)
                fixes.append("Удалены пробелы в конце строк")
            
            # Исправление отступов
            if re.search(r'\t', content):
                content = content.replace('\t', '    ')
                fixes.append("Табы заменены на пробелы")
            
            # Добавление пустой строки в конец
            if not content.endswith('\n'):
                content += '\n'
                fixes.append("Добавлена пустая строка в конец")
            
            # Исправление двойных пустых строк
            content = re.sub(r'\n\n\n+', '\n\n', content)
            if content != original:
                fixes.append("Убраны лишние пустые строки")
            
            # Исправление импортов
            lines = content.split('\n')
            import_lines = []
            other_lines = []
            
            for line in lines:
                if line.strip().startswith(('import ', 'from ')):
                    import_lines.append(line)
                else:
                    other_lines.append(line)
            
            if import_lines:
                import_lines.sort()
                content = '\n'.join(import_lines + [''] + other_lines)
                fixes.append("Отсортированы импорты")
            
            if content != original:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.fixes_applied.append({
                    "file": str(file_path),
                    "fixes": fixes
                })
                return True
                
        except Exception as e:
            print(f"Ошибка исправления {file_path}: {e}")
        
        return False
    
    def fix_directory(self, directory):
        fixed_count = 0
        for file_path in Path(directory).rglob("*.py"):
            if any(part in {".venv", "__pycache__", ".git"} for part in file_path.parts):
                continue
            
            if self.fix_file(file_path):
                fixed_count += 1
        
        return fixed_count
    
    def generate_report(self):
        return {
            "fixes_applied": len(self.fixes_applied),
            "details": self.fixes_applied
        }

def main():
    fixer = AutoFixerAgent()
    fixed = fixer.fix_directory(Path.cwd())
    print(f"Исправлено файлов: {fixed}")

if __name__ == "__main__":
    main()