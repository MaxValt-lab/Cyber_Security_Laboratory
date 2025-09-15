#!/usr/bin/env python3
import json
import time
from pathlib import Path
from datetime import datetime
from .code_analyzer_agent import CodeAnalyzerAgent
from .auto_fixer_agent import AutoFixerAgent
from .security_scanner_agent import SecurityScannerAgent

class AgentManager:
    def __init__(self):
        self.agents = {
            'analyzer': CodeAnalyzerAgent(),
            'fixer': AutoFixerAgent(),
            'security': SecurityScannerAgent()
        }
        self.results = {}
    
    def run_full_scan(self, directory=None):
        if directory is None:
            directory = Path.cwd()
        
        print(f"Запуск полного сканирования: {directory}")
        start_time = time.time()
        
        # 1. Анализ кода
        print("1. Анализ кода...")
        self.agents['analyzer'].scan_directory(directory)
        analyzer_report = self.agents['analyzer'].generate_report()
        
        # 2. Сканирование безопасности
        print("2. Сканирование безопасности...")
        self.agents['security'].scan_directory(directory)
        security_report = self.agents['security'].generate_report()
        
        # 3. Автоисправление
        print("3. Автоисправление...")
        fixed_count = self.agents['fixer'].fix_directory(directory)
        fixer_report = self.agents['fixer'].generate_report()
        
        end_time = time.time()
        
        # Сводный отчет
        self.results = {
            "scan_time": datetime.now().isoformat(),
            "duration": round(end_time - start_time, 2),
            "directory": str(directory),
            "code_analysis": analyzer_report,
            "security_scan": security_report,
            "auto_fixes": fixer_report,
            "summary": {
                "files_scanned": analyzer_report['statistics']['files_scanned'],
                "total_issues": analyzer_report['statistics']['issues_found'],
                "security_vulnerabilities": security_report['total_vulnerabilities'],
                "files_fixed": fixed_count
            }
        }
        
        return self.results
    
    def save_combined_report(self, filename="combined_analysis_report.json"):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        return filename
    
    def get_critical_issues(self):
        critical = []
        
        # Критические проблемы из анализатора
        if 'code_analysis' in self.results:
            for issue in self.results['code_analysis']['issues']:
                if issue['severity'] == 'HIGH':
                    critical.append(issue)
        
        # Критические уязвимости
        if 'security_scan' in self.results:
            for vuln in self.results['security_scan']['vulnerabilities']:
                if vuln['severity'] == 'CRITICAL':
                    critical.append(vuln)
        
        return critical
    
    def print_summary(self):
        if not self.results:
            print("Сканирование не выполнено")
            return
        
        summary = self.results['summary']
        print(f"\n{'='*50}")
        print(f"СВОДКА АНАЛИЗА КОДА")
        print(f"{'='*50}")
        print(f"Время сканирования: {self.results['duration']} сек")
        print(f"Файлов проверено: {summary['files_scanned']}")
        print(f"Проблем найдено: {summary['total_issues']}")
        print(f"Уязвимостей: {summary['security_vulnerabilities']}")
        print(f"Файлов исправлено: {summary['files_fixed']}")
        
        # Критические проблемы
        critical = self.get_critical_issues()
        if critical:
            print(f"\nКРИТИЧЕСКИЕ ПРОБЛЕМЫ ({len(critical)}):")
            for issue in critical[:5]:  # Показать первые 5
                print(f"  {issue['file']}:{issue['line']} - {issue['message']}")
        
        print(f"{'='*50}")

def main():
    manager = AgentManager()
    
    # Запуск полного сканирования
    results = manager.run_full_scan()
    
    # Сохранение отчета
    report_file = manager.save_combined_report()
    
    # Вывод сводки
    manager.print_summary()
    
    print(f"\nПолный отчет сохранен: {report_file}")

if __name__ == "__main__":
    main()