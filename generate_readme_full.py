#!/usr/bin/env python3
import os
from pathlib import Path
import sys

# Если путь передан как аргумент, используем его; иначе текущая папка
if len(sys.argv) > 1:
    ROOT_DIR = Path(sys.argv[1]).resolve()
else:
    ROOT_DIR = Path(__file__).resolve().parent

OUTPUT_FILE = ROOT_DIR / "README.md"

IGNORE = {".git", "__pycache__", ".idea", ".vscode", "node_modules", ".pytest_cache"}

# Описание директорий
DESCRIPTIONS = {
    "compliance": "Внешние стандарты и регуляторные требования (ФСТЭК, ФСБ, МВД, ГОСТ).",
    "deployment": "Инфраструктурный код и автоматизация (Terraform, Ansible, Docker, K8s).",
    "observability": "Мониторинг и наблюдаемость (Prometheus, Grafana, ELK).",
    "secrets": "Управление секретами: шаблоны и политики доступа.",
    "third_party": "Сторонние зависимости: SDK и библиотеки.",
    "security": "Политики ИБ, сканы, тестирование безопасности.",
    "examples": "Примеры и демонстрации: quickstart и демо.",
    "common": "Общие компоненты проекта (код, тесты, логирование, документация).",
    "vision-le": "Разные редакции продукта (Lite, Base, Pro², Pro³).",
    "collaboration": "Средства для совместной работы (чат).",
    "tools": "Вспомогательные скрипты и утилиты.",
    "ci": "Конфигурации CI/CD (GitLab, Jenkins, Azure).",
    "docs": "Общая документация: архитектура, гайды.",
}

PROJECT_DESCRIPTION = """**Cyber_Security_Laboratory** — это интеллектуальная система безопасности нового поколения, объединяющая киберзащиту и физический контроль.

Система предназначена для:
- 🏢 Охраны помещений с массовым пребыванием людей.
- 🌐 Защиты серверов и веб-сайтов.
- 🕵️ Мониторинга сетей Darknet.

Основные возможности:
- 👁 Распознавание лиц в реальном времени.
- 🚶 Отслеживание перемещений и скоплений людей.
- 🖥 Защита серверов и веб-сервисов.
- 🌐 Darknet-мониторинг.
- 📡 DevSecOps интеграция.
- 🧾 Соответствие требованиям регуляторов (ФСТЭК, ФСБ, ГОСТ, МВД).
"""

def build_tree(path: Path, prefix: str = "") -> str:
    entries = sorted([e for e in path.iterdir() if e.name not in IGNORE],
                     key=lambda x: (x.is_file(), x.name.lower()))
    tree = ""
    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        tree += f"{prefix}{connector}{entry.name}\n"
        if entry.is_dir():
            extension = "    " if i == len(entries) - 1 else "│   "
            tree += build_tree(entry, prefix + extension)
    return tree

def build_mermaid(path: Path, prefix: str = "  ") -> str:
    entries = sorted([e for e in path.iterdir() if e.name not in IGNORE],
                     key=lambda x: (x.is_file(), x.name.lower()))
    diagram = ""
    for entry in entries:
        diagram += f"{prefix}{entry.name}\n"
        if entry.is_dir():
            diagram += build_mermaid(entry, prefix + "  ")
    return diagram

def create_readmes():
    for folder, desc in DESCRIPTIONS.items():
        dir_path = ROOT_DIR / folder
        if dir_path.exists() and dir_path.is_dir():
            readme_path = dir_path / "README.md"
            if not readme_path.exists():
                with open(readme_path, "w", encoding="utf-8") as f:
                    f.write(f"# {folder}/\n\n{desc}\n")
                print(f"[OK] Создан {readme_path}")

def main():
    tree = build_tree(ROOT_DIR)
    mermaid = "```mermaid\nmindmap\n  root((Cyber_Security_Laboratory))\n"
    mermaid += build_mermaid(ROOT_DIR, "    ")
    mermaid += "```\n"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 🛡 Cyber_Security_Laboratory\n\n")
        f.write(f"{PROJECT_DESCRIPTION}\n\n")
        f.write("## 🗂 Структура проекта\n\n")
        f.write("### Дерево проекта\n```\n")
        f.write(f"{ROOT_DIR.name}/\n")
        f.write(tree)
        f.write("```\n\n")
        f.write("### Mindmap (Mermaid)\n")
        f.write(mermaid + "\n")
        f.write("### 📖 Описание директорий\n\n")
        f.write("| Директория | Назначение |\n")
        f.write("|------------|------------|\n")
        for folder, desc in DESCRIPTIONS.items():
            f.write(f"| `{folder}/` | {desc} |\n")

    print(f"[OK] Главный README создан в {OUTPUT_FILE}")
    create_readmes()

if __name__ == "__main__":
    main()
