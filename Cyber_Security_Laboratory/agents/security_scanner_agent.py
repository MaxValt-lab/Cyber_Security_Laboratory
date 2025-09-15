#!/usr/bin/env python3
import re
import json
from pathlib import Path
from datetime import datetime

class SecurityScannerAgent:
    def __init__(self):
        self.vulnerabilities = []
        self.security_patterns = {
            'sql_injection': [
                r'execute\s*\(\s*["\'].*%.*["\']',
                r'cursor\.execute\s*\(\s*["\'].*\+.*["\']',
                r'query\s*=\s*["\'].*%.*["\']'
            ],
            'command_injection': [
                r'os\.system\s*\(',
                r'subprocess\.call\s*\([^)]*shell\s*=\s*True',
                r'eval\s*\(',
                r'exec\s*\('
            ],
            'hardcoded_secrets': [
                r'password\s*=\s*["\'][^"\']{8,}["\']',
                r'api_key\s*=\s*["\'][^"\']{16,}["\']',
                r'secret\s*=\s*["\'][^"\']{8,}["\']',
                r'token\s*=\s*["\'][^"\']{16,}["\']'
            ],
            'unsafe_deserialization': [
                r'pickle\.loads?\s*\(',
                r'yaml\.load\s*\(',
                r'json\.loads?\s*\([^)]*\)'
            ],
            'path_traversal': [
                r'open\s*\([^)]*\.\./.*\)',
                r'file\s*\([^)]*\.\./.*\)'
            ]
        }
    
    def scan_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for vuln_type, patterns in self.security_patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        self._add_vulnerability(file_path, vuln_type, pattern, line_num, match.group())
                        
        except Exception as e:
            print(f"Ошибка сканирования {file_path}: {e}")
    
    def _add_vulnerability(self, file_path, vuln_type, pattern, line_num, code_snippet):
        severity = self._get_severity(vuln_type)
        
        vulnerability = {
            "file": str(file_path),
            "type": vuln_type,
            "severity": severity,
            "line": line_num,
            "pattern": pattern,
            "code": code_snippet.strip(),
            "timestamp": datetime.now().isoformat(),
            "description": self._get_description(vuln_type)
        }
        
        self.vulnerabilities.append(vulnerability)
    
    def _get_severity(self, vuln_type):
        severity_map = {
            'sql_injection': 'CRITICAL',
            'command_injection': 'CRITICAL',
            'hardcoded_secrets': 'HIGH',
            'unsafe_deserialization': 'HIGH',
            'path_traversal': 'MEDIUM'
        }
        return severity_map.get(vuln_type, 'LOW')
    
    def _get_description(self, vuln_type):
        descriptions = {
            'sql_injection': 'Возможная SQL инъекция',
            'command_injection': 'Возможная инъекция команд',
            'hardcoded_secrets': 'Секреты в коде',
            'unsafe_deserialization': 'Небезопасная десериализация',
            'path_traversal': 'Возможный path traversal'
        }
        return descriptions.get(vuln_type, 'Неизвестная уязвимость')
    
    def scan_directory(self, directory):
        for file_path in Path(directory).rglob("*.py"):
            if any(part in {".venv", "__pycache__", ".git"} for part in file_path.parts):
                continue
            self.scan_file(file_path)
    
    def generate_report(self):
        critical = len([v for v in self.vulnerabilities if v['severity'] == 'CRITICAL'])
        high = len([v for v in self.vulnerabilities if v['severity'] == 'HIGH'])
        medium = len([v for v in self.vulnerabilities if v['severity'] == 'MEDIUM'])
        
        return {
            "scan_time": datetime.now().isoformat(),
            "total_vulnerabilities": len(self.vulnerabilities),
            "severity_breakdown": {
                "critical": critical,
                "high": high,
                "medium": medium
            },
            "vulnerabilities": self.vulnerabilities
        }
    
    def save_report(self, filename="security_report.json"):
        report = self.generate_report()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        return filename

def main():
    scanner = SecurityScannerAgent()
    scanner.scan_directory(Path.cwd())
    
    report_file = scanner.save_report()
    report = scanner.generate_report()
    
    print(f"Отчет безопасности: {report_file}")
    print(f"Найдено уязвимостей: {report['total_vulnerabilities']}")
    print(f"Критических: {report['severity_breakdown']['critical']}")
    print(f"Высоких: {report['severity_breakdown']['high']}")

if __name__ == "__main__":
    main()