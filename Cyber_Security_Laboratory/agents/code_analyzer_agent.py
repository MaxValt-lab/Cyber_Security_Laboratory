#!/usr/bin/env python3
import os
import ast
import re
import json
from pathlib import Path
from datetime import datetime

class CodeAnalyzerAgent:
    def __init__(self):
        self.issues = []
        self.stats = {"files_scanned": 0, "issues_found": 0, "critical_issues": 0}
        
    def scan_directory(self, directory):
        for file_path in Path(directory).rglob("*.py"):
            if self._should_skip_file(file_path):
                continue
            self._analyze_file(file_path)
            self.stats["files_scanned"] += 1
        
    def _should_skip_file(self, file_path):
        skip_dirs = {".venv", "__pycache__", ".git"}
        return any(part in skip_dirs for part in file_path.parts)
    
    def _analyze_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self._check_syntax(file_path, content)
            self._check_security(file_path, content)
            self._check_quality(file_path, content)
            
        except Exception as e:
            self._add_issue(file_path, "ERROR", f"Ошибка чтения: {e}", 1)
    
    def _check_syntax(self, file_path, content):
        try:
            ast.parse(content)
        except SyntaxError as e:
            self._add_issue(file_path, "SYNTAX", f"Синтаксическая ошибка: {e.msg}", e.lineno)
    
    def _check_security(self, file_path, content):
        patterns = [
            (r'eval\s*\(', "eval() небезопасно"),
            (r'exec\s*\(', "exec() небезопасно"),
            (r'password\s*=\s*["\'][^"\']+["\']', "Пароль в коде"),
            (r'api_key\s*=\s*["\'][^"\']+["\']', "API ключ в коде"),
        ]
        
        for i, line in enumerate(content.split('\n'), 1):
            for pattern, message in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self._add_issue(file_path, "SECURITY", message, i)
    
    def _check_quality(self, file_path, content):
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                self._add_issue(file_path, "QUALITY", f"Длинная строка ({len(line)})", i)
            
            if re.search(r'#\s*TODO', line, re.IGNORECASE):
                self._add_issue(file_path, "TODO", "Незавершенная задача", i)
    
    def _add_issue(self, file_path, issue_type, message, line_number):
        severity = "HIGH" if issue_type == "SECURITY" else "MEDIUM" if issue_type == "SYNTAX" else "LOW"
        
        issue = {
            "file": str(file_path),
            "type": issue_type,
            "severity": severity,
            "message": message,
            "line": line_number,
            "timestamp": datetime.now().isoformat()
        }
        
        self.issues.append(issue)
        self.stats["issues_found"] += 1
        
        if severity == "HIGH":
            self.stats["critical_issues"] += 1
    
    def generate_report(self):
        return {
            "scan_time": datetime.now().isoformat(),
            "statistics": self.stats,
            "issues": self.issues
        }
    
    def save_report(self, filename="code_analysis_report.json"):
        report = self.generate_report()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        return filename
    
    def auto_fix(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            content = re.sub(r' +\n', '\n', content)  # Убрать пробелы в конце строк
            content = re.sub(r'  +', ' ', content)    # Убрать двойные пробелы
            
            if not content.endswith('\n'):
                content += '\n'
            
            if content != original:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
                
        except Exception:
            pass
        
        return False

def main():
    analyzer = CodeAnalyzerAgent()
    analyzer.scan_directory(Path.cwd())
    
    report_file = analyzer.save_report()
    print(f"Отчет: {report_file}")
    print(f"Файлов: {analyzer.stats['files_scanned']}")
    print(f"Проблем: {analyzer.stats['issues_found']}")
    print(f"Критических: {analyzer.stats['critical_issues']}")

if __name__ == "__main__":
    main()