#!/usr/bin/env python3
"""
Скрипт запуска Cyber Security Laboratory
"""
import os
import sys
import uvicorn
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def main():
    # Инициализация базы данных
    from database import db
    print("✅ База данных инициализирована")
    
    # Проверка конфигурации
    from servise.config import RISK_POLICY_PATH
    if not os.path.exists(RISK_POLICY_PATH):
        print(f"⚠️  Файл политики рисков не найден: {RISK_POLICY_PATH}")
        print("   Будет использована базовая конфигурация")
    
    # Запуск сервера
    print("🚀 Запуск Cyber Security Laboratory...")
    print("📊 API доступно по адресу: http://localhost:8000")
    print("📖 Документация: http://localhost:8000/docs")
    
    uvicorn.run(
        "servise.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()