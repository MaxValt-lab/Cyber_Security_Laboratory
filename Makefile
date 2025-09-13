# 🧪 Тестирование
test:
    pytest --cov=common/src --cov-report=term-missing

test-html:
    pytest --cov=common/src --cov-report=html

# 🔍 Линтеры и типы
lint:
    ruff check .
    mypy common/src

# 🔐 Безопасность
security:
    bandit -r common/src -f json -o bandit.json
    safety check --full-report > safety-report.json
    gitleaks detect --source . --report-path gitleaks-report.json

# 📦 SBOM
sbom:
    cyclonedx-py requirements -o sbom.json

# 🐳 Docker
docker:
    docker build -f deployment/docker/Dockerfile -t cyberlab:latest .

docker-run:
    docker run --rm cyberlab:latest

# 🧹 Очистка артефактов
clean:
    rm -rf .pytest_cache/ htmlcov/ .coverage sbom.json gitleaks-report.json safety-report.json bandit.json

# 🔁 Всё сразу
all: lint test security sbom docker

make lint         # Проверка стиля и типов
make test         # Запуск тестов с покрытием
make test-html    # HTML-отчёт покрытия
make security     # Сканирование безопасности
make sbom         # Генерация SBOM
make docker       # Сборка Docker-образа
make docker-run   # Запуск контейнера
make clean        # Очистка артефактов
make all          # Всё сразу

check-license:
	python license_check.py