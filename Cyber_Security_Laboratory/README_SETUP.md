# 🚀 Автоматическая установка и запуск

## Быстрый старт (Windows)

### Вариант 1: Полная автоматизация
```cmd
run_all.bat
```

### Вариант 2: Пошаговая установка
```cmd
# 1. Установка
setup.bat

# 2. Запуск
start.bat

# 3. Тестирование (в новом окне)
test.bat
```

## Ручная установка

### 1. Установка зависимостей
```cmd
py install.py
```

### 2. Запуск системы
```cmd
py start.py
```

### 3. Тестирование
```cmd
py test_simple.py
```

## Доступные интерфейсы

- **Веб-интерфейс**: http://localhost:8000
- **API документация**: http://localhost:8000/docs
- **Статус API**: http://localhost:8000/api/status

## Структура файлов

```
├── run_all.bat          # Полная автоматизация
├── setup.bat            # Установка окружения
├── start.bat            # Запуск системы
├── test.bat             # Тестирование
├── install.py           # Python установщик
├── start.py             # Основной сервер
├── test_simple.py       # Тестовый клиент
├── requirements-minimal.txt  # Минимальные зависимости
└── .env.example         # Пример конфигурации
```

## Решение проблем

### Python не найден
- Установите Python 3.8+ с python.org
- Убедитесь, что Python добавлен в PATH

### Порт занят
- Измените PORT в start.py
- Или завершите процесс на порту 8000

### Ошибки зависимостей
- Запустите setup.bat заново
- Проверьте подключение к интернету

## Тестирование API

После запуска системы:

```bash
# Проверка статуса
curl http://localhost:8000/api/status

# Отправка события
curl -X POST http://localhost:8000/api/event \
  -H "Content-Type: application/json" \
  -d '{"type":"test","source":"manual","severity":"low","message":"Test event"}'

# Получение статистики
curl http://localhost:8000/api/stats
```