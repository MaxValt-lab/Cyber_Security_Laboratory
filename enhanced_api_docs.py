"""
Расширенная API документация с примерами
"""
import json
from datetime import datetime

class APIDocumentationGenerator:
    def __init__(self):
        self.api_version = "2.0.0"
        self.base_url = "http://localhost:8089"
        
    def generate_complete_api_docs(self):
        """Генерация полной API документации"""
        api_docs = {
            "openapi": "3.0.0",
            "info": {
                "title": "Director Management System API",
                "version": self.api_version,
                "description": "Комплексная система управления директора с безопасностью и аналитикой",
                "contact": {
                    "name": "System Administrator",
                    "email": "admin@company.com"
                }
            },
            "servers": [
                {
                    "url": self.base_url,
                    "description": "Локальный сервер разработки"
                }
            ],
            "paths": self._generate_api_paths(),
            "components": self._generate_components(),
            "security": [
                {
                    "sessionAuth": []
                }
            ]
        }
        
        return api_docs
    
    def _generate_api_paths(self):
        """Генерация путей API"""
        return {
            "/api/login": {
                "post": {
                    "summary": "Аутентификация пользователя",
                    "description": "Вход в систему с проверкой учетных данных",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/LoginRequest"
                                },
                                "example": {
                                    "username": "director",
                                    "password": "admin2024"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Успешная аутентификация",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/LoginResponse"
                                    },
                                    "example": {
                                        "success": True,
                                        "session_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                                        "user_id": 1,
                                        "role": "admin",
                                        "requires_mfa": True
                                    }
                                }
                            }
                        },
                        "401": {
                            "description": "Неверные учетные данные",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "success": False,
                                        "error": "Invalid credentials"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/2fa/setup": {
                "post": {
                    "summary": "Настройка двухфакторной аутентификации",
                    "security": [{"sessionAuth": []}],
                    "responses": {
                        "200": {
                            "description": "QR код для настройки 2FA",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
                                        "secret": "JBSWY3DPEHPK3PXP",
                                        "backup_codes": ["12345678", "87654321"]
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/dashboard/metrics": {
                "get": {
                    "summary": "Системные метрики",
                    "security": [{"sessionAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Текущие метрики системы",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "cpu_percent": 45.2,
                                        "memory_percent": 62.1,
                                        "disk_percent": 78.5,
                                        "active_connections": 12,
                                        "uptime": 86400
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/projects": {
                "get": {
                    "summary": "Список проектов",
                    "security": [{"sessionAuth": []}],
                    "parameters": [
                        {
                            "name": "status",
                            "in": "query",
                            "schema": {"type": "string", "enum": ["active", "completed", "paused"]},
                            "description": "Фильтр по статусу проекта"
                        },
                        {
                            "name": "limit",
                            "in": "query",
                            "schema": {"type": "integer", "default": 10},
                            "description": "Количество проектов на странице"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Список проектов",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "projects": [
                                            {
                                                "id": 1,
                                                "name": "Строительство офисного центра",
                                                "status": "active",
                                                "budget": 5000000,
                                                "progress": 65,
                                                "deadline": "2024-06-15"
                                            }
                                        ],
                                        "total": 12,
                                        "page": 1
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "summary": "Создание нового проекта",
                    "security": [{"sessionAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ProjectCreate"
                                },
                                "example": {
                                    "name": "Новый жилой комплекс",
                                    "description": "Строительство 3-этажного жилого дома",
                                    "budget": 8000000,
                                    "deadline": "2024-12-31",
                                    "manager_id": 2
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Проект создан",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "id": 13,
                                        "message": "Проект успешно создан"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/notifications": {
                "get": {
                    "summary": "Получение уведомлений",
                    "security": [{"sessionAuth": []}],
                    "parameters": [
                        {
                            "name": "unread_only",
                            "in": "query",
                            "schema": {"type": "boolean", "default": False},
                            "description": "Только непрочитанные уведомления"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Список уведомлений",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "notifications": [
                                            {
                                                "id": 1,
                                                "title": "Новая задача",
                                                "message": "Назначена новая задача по проекту А",
                                                "type": "task",
                                                "priority": 2,
                                                "created_at": "2024-01-15T10:30:00",
                                                "is_read": False
                                            }
                                        ],
                                        "unread_count": 3
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/analytics/revenue": {
                "get": {
                    "summary": "Аналитика по выручке",
                    "security": [{"sessionAuth": []}],
                    "parameters": [
                        {
                            "name": "period",
                            "in": "query",
                            "schema": {"type": "string", "enum": ["day", "week", "month", "year"]},
                            "description": "Период для анализа"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Данные по выручке",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "period": "month",
                                        "total_revenue": 2500000,
                                        "revenue_by_project": [
                                            {"project_id": 1, "revenue": 1200000},
                                            {"project_id": 2, "revenue": 800000}
                                        ],
                                        "growth_rate": 15.5
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/security/audit": {
                "get": {
                    "summary": "Журнал аудита",
                    "security": [{"sessionAuth": []}],
                    "parameters": [
                        {
                            "name": "action",
                            "in": "query",
                            "schema": {"type": "string"},
                            "description": "Фильтр по типу действия"
                        },
                        {
                            "name": "date_from",
                            "in": "query",
                            "schema": {"type": "string", "format": "date"},
                            "description": "Начальная дата"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Записи аудита",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "audit_entries": [
                                            {
                                                "timestamp": "2024-01-15T10:30:00",
                                                "user": "director",
                                                "action": "login_success",
                                                "resource": "authentication",
                                                "ip_address": "192.168.1.100",
                                                "success": True
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    
    def _generate_components(self):
        """Генерация компонентов схемы"""
        return {
            "schemas": {
                "LoginRequest": {
                    "type": "object",
                    "required": ["username", "password"],
                    "properties": {
                        "username": {"type": "string", "description": "Имя пользователя"},
                        "password": {"type": "string", "description": "Пароль"}
                    }
                },
                "LoginResponse": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "session_token": {"type": "string"},
                        "user_id": {"type": "integer"},
                        "role": {"type": "string"},
                        "requires_mfa": {"type": "boolean"}
                    }
                },
                "ProjectCreate": {
                    "type": "object",
                    "required": ["name", "budget", "deadline"],
                    "properties": {
                        "name": {"type": "string", "description": "Название проекта"},
                        "description": {"type": "string", "description": "Описание проекта"},
                        "budget": {"type": "number", "description": "Бюджет проекта"},
                        "deadline": {"type": "string", "format": "date", "description": "Срок завершения"},
                        "manager_id": {"type": "integer", "description": "ID менеджера проекта"}
                    }
                },
                "Error": {
                    "type": "object",
                    "properties": {
                        "error": {"type": "string", "description": "Описание ошибки"},
                        "code": {"type": "integer", "description": "Код ошибки"}
                    }
                }
            },
            "securitySchemes": {
                "sessionAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                    "description": "Токен сессии для аутентификации"
                }
            }
        }
    
    def generate_usage_examples(self):
        """Примеры использования API"""
        examples = {
            "authentication": {
                "description": "Аутентификация и получение токена сессии",
                "curl": """curl -X POST http://localhost:8089/api/login \\
  -H "Content-Type: application/json" \\
  -d '{"username": "director", "password": "admin2024"}'""",
                "python": """import requests

response = requests.post('http://localhost:8089/api/login', 
                        json={'username': 'director', 'password': 'admin2024'})
data = response.json()
session_token = data['session_token']""",
                "javascript": """fetch('http://localhost:8089/api/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({username: 'director', password: 'admin2024'})
})
.then(response => response.json())
.then(data => console.log(data.session_token));"""
            },
            "get_projects": {
                "description": "Получение списка активных проектов",
                "curl": """curl -X GET "http://localhost:8089/api/projects?status=active&limit=5" \\
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" """,
                "python": """headers = {'Authorization': f'Bearer {session_token}'}
response = requests.get('http://localhost:8089/api/projects', 
                       params={'status': 'active', 'limit': 5},
                       headers=headers)
projects = response.json()['projects']""",
                "javascript": """fetch('http://localhost:8089/api/projects?status=active&limit=5', {
  headers: {'Authorization': `Bearer ${sessionToken}`}
})
.then(response => response.json())
.then(data => console.log(data.projects));"""
            },
            "create_project": {
                "description": "Создание нового проекта",
                "curl": """curl -X POST http://localhost:8089/api/projects \\
  -H "Authorization: Bearer YOUR_SESSION_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Новый проект",
    "description": "Описание проекта",
    "budget": 5000000,
    "deadline": "2024-12-31",
    "manager_id": 2
  }'""",
                "python": """project_data = {
    'name': 'Новый проект',
    'description': 'Описание проекта',
    'budget': 5000000,
    'deadline': '2024-12-31',
    'manager_id': 2
}

response = requests.post('http://localhost:8089/api/projects',
                        json=project_data,
                        headers=headers)""",
                "javascript": """const projectData = {
  name: 'Новый проект',
  description: 'Описание проекта',
  budget: 5000000,
  deadline: '2024-12-31',
  manager_id: 2
};

fetch('http://localhost:8089/api/projects', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${sessionToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(projectData)
});"""
            }
        }
        
        return examples
    
    def generate_error_codes(self):
        """Коды ошибок API"""
        return {
            "400": {
                "description": "Неверный запрос",
                "examples": [
                    "Отсутствуют обязательные параметры",
                    "Неверный формат данных",
                    "Валидация не пройдена"
                ]
            },
            "401": {
                "description": "Не авторизован",
                "examples": [
                    "Отсутствует токен аутентификации",
                    "Недействительный токен",
                    "Токен истек"
                ]
            },
            "403": {
                "description": "Доступ запрещен",
                "examples": [
                    "Недостаточно прав доступа",
                    "Аккаунт заблокирован",
                    "Ресурс недоступен для данной роли"
                ]
            },
            "404": {
                "description": "Не найдено",
                "examples": [
                    "Ресурс не существует",
                    "Неверный URL",
                    "Удаленный объект"
                ]
            },
            "429": {
                "description": "Слишком много запросов",
                "examples": [
                    "Превышен лимит запросов",
                    "Временная блокировка",
                    "Rate limiting активен"
                ]
            },
            "500": {
                "description": "Внутренняя ошибка сервера",
                "examples": [
                    "Ошибка базы данных",
                    "Системная ошибка",
                    "Недоступность сервиса"
                ]
            }
        }
    
    def save_documentation(self, output_dir="docs/api"):
        """Сохранение документации"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # OpenAPI спецификация
        api_docs = self.generate_complete_api_docs()
        with open(f"{output_dir}/openapi.json", 'w', encoding='utf-8') as f:
            json.dump(api_docs, f, indent=2, ensure_ascii=False)
        
        # Примеры использования
        examples = self.generate_usage_examples()
        with open(f"{output_dir}/examples.json", 'w', encoding='utf-8') as f:
            json.dump(examples, f, indent=2, ensure_ascii=False)
        
        # Коды ошибок
        error_codes = self.generate_error_codes()
        with open(f"{output_dir}/error_codes.json", 'w', encoding='utf-8') as f:
            json.dump(error_codes, f, indent=2, ensure_ascii=False)
        
        print(f"📚 API документация сохранена в {output_dir}")

if __name__ == "__main__":
    generator = APIDocumentationGenerator()
    generator.save_documentation()