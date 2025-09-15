# 🚀 Быстрый запуск Cyber Security Laboratory

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск системы

```bash
python start.py
```

## Доступные интерфейсы

- **Веб-интерфейс**: http://localhost:8000
- **API документация**: http://localhost:8000/docs
- **API статус**: http://localhost:8000/api/status

## Тестирование

```bash
# В новом терминале
python test_client.py
```

## API Endpoints

### Основные
- `POST /api/event` - Отправка события
- `GET /api/status` - Статус системы
- `GET /api/health` - Проверка здоровья

### Мониторинг
- `GET /api/events` - Список событий
- `GET /api/incidents` - Список инцидентов  
- `GET /api/stats` - Статистика

## Пример события

```json
{
  "type": "login_attempt",
  "source": "external", 
  "severity": "medium",
  "message": "Неудачная попытка входа"
}
```

## Конфигурация

Скопируйте `.env.example` в `.env` и настройте переменные окружения.

## Docker

```bash
docker build -t cyberlab .
docker run -p 8000:8000 cyberlab
```