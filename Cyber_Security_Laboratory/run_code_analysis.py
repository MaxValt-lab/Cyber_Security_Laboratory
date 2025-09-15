#!/usr/bin/env python3
"""
Запуск автоматического анализа кода
"""
import sys
from pathlib import Path

# Добавляем путь к агентам
sys.path.append(str(Path(__file__).parent))

from agents.code_analyzer_agent import CodeAnalyzerAgent
from agents.security_scanner_agent import SecurityScannerAgent
from agents.auto_fixer_agent import AutoFixerAgent

def main():
    print("🤖 Запуск автоматического анализа кода")
    print("="*50)
    
    # 1. Анализ кода
    print("📊 Анализ качества кода...")
    analyzer = CodeAnalyzerAgent()
    analyzer.scan_directory(Path.cwd())
    analyzer.save_report("code_analysis.json")
    
    print(f"   Файлов: {analyzer.stats['files_scanned']}")
    print(f"   Проблем: {analyzer.stats['issues_found']}")
    
    # 2. Сканирование безопасности
    print("\n🔒 Сканирование безопасности...")
    security = SecurityScannerAgent()
    security.scan_directory(Path.cwd())
    security.save_report("security_scan.json")
    
    report = security.generate_report()
    print(f"   Уязвимостей: {report['total_vulnerabilities']}")
    print(f"   Критических: {report['severity_breakdown']['critical']}")
    
    # 3. Автоисправление
    print("\n🔧 Автоисправление...")
    fixer = AutoFixerAgent()
    fixed = fixer.fix_directory(Path.cwd())
    
    print(f"   Исправлено файлов: {fixed}")
    
    # Сводка
    print("\n" + "="*50)
    print("✅ АНАЛИЗ ЗАВЕРШЕН")
    print(f"📁 Отчеты: code_analysis.json, security_scan.json")
    
    # Показать критические проблемы
    critical_issues = [i for i in analyzer.issues if i["severity"] == "HIGH"]
    critical_vulns = [v for v in security.vulnerabilities if v["severity"] == "CRITICAL"]
    
    if critical_issues or critical_vulns:
        print("\n⚠️  КРИТИЧЕСКИЕ ПРОБЛЕМЫ:")
        for issue in (critical_issues + critical_vulns)[:5]:
            print(f"   {issue['file']}:{issue['line']} - {issue.get('message', issue.get('description'))}")

if __name__ == "__main__":
    main()