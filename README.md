# 🛡 Cyber_Security_Laboratory

**Cyber_Security_Laboratory** — это интеллектуальная система безопасности нового поколения, объединяющая киберзащиту и физический контроль.

---

## 🎯 Назначение

- 🏢 Охрана помещений с массовым пребыванием людей  
  *(бизнес-центры, ТРЦ, аэропорты, стадионы)*  
- 🌐 Защита серверов и веб-сайтов  
  *(IDS/IPS, анализ логов, фильтрация трафика)*  
- 🕵️ Мониторинг сетей Darknet  
  *(выявление утечек данных и подготовительных действий для атак)*  

---

## ⚙️ Основные возможности

- 👁 Распознавание лиц в реальном времени  
- 🚶 Отслеживание перемещений и скоплений людей  
- 🖥 Защита серверов и веб-сервисов  
- 🌐 Darknet-мониторинг  
- 📡 DevSecOps-интеграция (CI/CD с проверками безопасности)  
- 🧾 Соответствие требованиям регуляторов (ФСТЭК, ФСБ, ГОСТ, МВД)  

---

## 👥 Целевая аудитория

- Государственные структуры и критическая инфраструктура  
- Крупные компании с высокой концентрацией людей  
- Центры обработки данных и серверные площадки  
- Онлайн-сервисы и финансовые организации  

---

## 🚀 Быстрый старт

```bash
git clone https://github.com/MaxValt-lab/Cyber_Security_Laboratory.git
cd Cyber_Security_Laboratory
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pre-commit install
pre-commit run --all-files
🧪 Тестирование
bash
pytest --cov=common/src --cov-report=term-missing
Для HTML-отчёта:

bash
pytest --cov=common/src --cov-report=html
🔐 Безопасность
bash
bandit -r common/src
safety check --full-report
gitleaks detect --source . --report-path gitleaks-report.json
Инструменты:

bandit — статический анализ Python-кода

safety — проверка зависимостей на CVE

gitleaks — поиск секретов в коде и истории

pre-commit — автоматические проверки при коммите

🐳 Docker
bash
docker build -f deployment/docker/Dockerfile -t cyberlab:latest .
docker run --rm cyberlab:latest
📦 SBOM
bash
cyclonedx-py requirements -o sbom.json
Файл sbom.json используется для соответствия требованиям регуляторов.

⚙️ CI/CD
Автоматизация через GitHub Actions:

.github/workflows/devsecops.yml — основной пайплайн

Этапы: lint → security → test → sbom → secrets → docker

Пайплайн запускается при каждом push и pull request в master.

📈 Мониторинг
Prometheus: /metrics endpoint

Grafana: дешборды из observability/grafana

ELK: централизованные логи

📤 Деплой
Docker Compose / Kubernetes (Helm/Kustomize)

Поддержка GitHub Environments: dev, stage

📜 Соответствие
Каталоги compliance/ содержат шаблоны и чек-листы

Генерация SBOM, аудит логов, контроль доступа

Поддержка требований ФСТЭК, ФСБ, МВД, ГОСТ

🗂 Структура проекта
text
Cyber_Security_Laboratory/
├── compliance/         # Регуляторные требования
├── deployment/         # Terraform, Ansible, Docker, K8s
├── observability/      # Prometheus, Grafana, ELK
├── secrets/            # Шаблоны и политики доступа
├── third_party/        # SDK и сторонние библиотеки
├── security/           # Политики, сканы, тесты
├── examples/           # Quickstart и демо
├── common/             # Код, тесты, логика, документация
├── vision-le/          # Lite, Base, Pro², Pro³ редакции
├── collaboration/      # Чат и совместная работа
├── tools/              # Утилиты и скрипты
├── ci/                 # GitLab, Jenkins, Azure конфиги
├── docs/               # Архитектура и гайды
├── .github/workflows/  # GitHub Actions пайплайны
├── CHANGELOG.md
├── VERSION
├── LICENSE
└── README.md
🧾 Лицензия
MIT License

🤝 Контакты
skrusich2000@gmail.com
Разработчик: Олег Журавлёв
Репозиторий: MaxValt-lab/Cyber_Security_Laboratory
