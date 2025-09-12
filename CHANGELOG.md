# Changelog

Все значимые изменения в этом проекте будут документироваться в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/), и этот проект придерживается [Semantic Versioning](https://semver.org/lang/ru/).

## [0.1.0] — 2025-09-12
### Добавлено
- Инициализация проекта: структура каталогов, базовые конфигурации
- `README.md`: описание назначения, возможностей и целевой аудитории
- `index.html`: адаптивный лендинг с баннером, навигацией, SBOM и формой обратной связи
- CI/CD пайплайн: `.github/workflows/devsecops.yml` с этапами lint → security → test → sbom → secrets → docker → release → deploy
- Безопасность: интеграция `bandit`, `safety`, `gitleaks`, `pre-commit`
- Мониторинг: Prometheus `/metrics`, Grafana дешборды, ELK
- SBOM: генерация через `cyclonedx-py`, файл `sbom.json`
- Структура проекта: compliance, deployment, observability, security, vision-le, tools, common
- Документация: `security.md`, `roadmap.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`

### Изменено
- `.gitignore`: добавлены исключения для виртуального окружения и отчётов
- `Makefile`: добавлены команды `make all`, `make release`, `make deploy`

### Удалено
- (пока ничего)

