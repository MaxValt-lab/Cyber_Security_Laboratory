"""
Строительный менеджер - управление проектами, материалами, рабочими
"""
import sqlite3
import json
from datetime import datetime, timedelta

class ConstructionManagerAgent:
    def __init__(self):
        self.setup_database()
        
    def setup_database(self):
        """Настройка базы данных строительства"""
        conn = sqlite3.connect('construction.db')
        cursor = conn.cursor()
        
        # Проекты
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT,
                type TEXT,
                status TEXT DEFAULT 'planning',
                budget REAL,
                start_date TEXT,
                end_date TEXT,
                progress INTEGER DEFAULT 0,
                manager_id INTEGER
            )
        ''')
        
        # Материалы
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS materials (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                unit TEXT,
                price_per_unit REAL,
                supplier TEXT,
                stock_quantity INTEGER DEFAULT 0,
                min_stock INTEGER DEFAULT 10
            )
        ''')
        
        # Рабочие
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                specialty TEXT,
                hourly_rate REAL,
                phone TEXT,
                status TEXT DEFAULT 'available',
                current_project_id INTEGER
            )
        ''')
        
        # Задачи
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                project_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                assigned_worker_id INTEGER,
                status TEXT DEFAULT 'pending',
                priority TEXT DEFAULT 'medium',
                start_date TEXT,
                due_date TEXT,
                completion_date TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Добавление тестовых данных
        self._add_sample_data()
    
    def _add_sample_data(self):
        """Добавление примеров данных"""
        conn = sqlite3.connect('construction.db')
        cursor = conn.cursor()
        
        # Проверка существования данных
        cursor.execute("SELECT COUNT(*) FROM projects")
        if cursor.fetchone()[0] == 0:
            # Проекты
            projects = [
                ("Офисный центр 'Альфа'", "ул. Ленина, 15", "commercial", "active", 15000000, "2024-01-15", "2024-08-15", 45, 1),
                ("Жилой комплекс 'Солнечный'", "ул. Мира, 22", "residential", "active", 25000000, "2024-02-01", "2024-12-01", 30, 2),
                ("Торговый центр 'Европа'", "пр. Победы, 8", "commercial", "planning", 35000000, "2024-03-01", "2025-01-01", 5, 1)
            ]
            
            cursor.executemany('''
                INSERT INTO projects (name, address, type, status, budget, start_date, end_date, progress, manager_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', projects)
            
            # Материалы
            materials = [
                ("Цемент М400", "тонна", 4500, "СтройМатериалы ООО", 50, 10),
                ("Кирпич красный", "тыс.шт", 12000, "КирпичЗавод", 25, 5),
                ("Арматура 12мм", "тонна", 45000, "МеталлТорг", 15, 3),
                ("Песок речной", "м³", 800, "ПескоГрав", 100, 20),
                ("Щебень 20-40", "м³", 1200, "ПескоГрав", 80, 15)
            ]
            
            cursor.executemany('''
                INSERT INTO materials (name, unit, price_per_unit, supplier, stock_quantity, min_stock)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', materials)
            
            # Рабочие
            workers = [
                ("Иванов Петр", "каменщик", 800, "+7-900-123-45-67", "busy", 1),
                ("Сидоров Иван", "электрик", 900, "+7-900-234-56-78", "available", None),
                ("Петров Алексей", "сантехник", 850, "+7-900-345-67-89", "busy", 2),
                ("Козлов Сергей", "маляр", 700, "+7-900-456-78-90", "available", None),
                ("Новиков Дмитрий", "прораб", 1200, "+7-900-567-89-01", "busy", 1)
            ]
            
            cursor.executemany('''
                INSERT INTO workers (name, specialty, hourly_rate, phone, status, current_project_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', workers)
            
            # Задачи
            tasks = [
                (1, "Заливка фундамента", "Подготовка и заливка фундамента здания", 1, "in_progress", "high", "2024-01-15", "2024-01-25", None),
                (1, "Возведение стен 1 этажа", "Кладка стен первого этажа", 1, "pending", "high", "2024-01-26", "2024-02-15", None),
                (2, "Прокладка электропроводки", "Монтаж электрической сети", 2, "pending", "medium", "2024-02-05", "2024-02-20", None),
                (2, "Установка сантехники", "Монтаж водопровода и канализации", 3, "pending", "medium", "2024-02-10", "2024-02-25", None)
            ]
            
            cursor.executemany('''
                INSERT INTO tasks (project_id, title, description, assigned_worker_id, status, priority, start_date, due_date, completion_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tasks)
        
        conn.commit()
        conn.close()
    
    def get_projects_overview(self):
        """Обзор всех проектов"""
        conn = sqlite3.connect('construction.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, address, type, status, budget, progress, start_date, end_date
            FROM projects ORDER BY start_date DESC
        ''')
        
        projects = []
        for row in cursor.fetchall():
            projects.append({
                "id": row[0],
                "name": row[1],
                "address": row[2],
                "type": row[3],
                "status": row[4],
                "budget": row[5],
                "progress": row[6],
                "start_date": row[7],
                "end_date": row[8]
            })
        
        conn.close()
        return projects
    
    def get_materials_status(self):
        """Статус материалов на складе"""
        conn = sqlite3.connect('construction.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT name, unit, stock_quantity, min_stock, price_per_unit, supplier
            FROM materials ORDER BY name
        ''')
        
        materials = []
        low_stock = []
        
        for row in cursor.fetchall():
            material = {
                "name": row[0],
                "unit": row[1],
                "stock": row[2],
                "min_stock": row[3],
                "price": row[4],
                "supplier": row[5],
                "status": "ok" if row[2] > row[3] else "low"
            }
            materials.append(material)
            
            if row[2] <= row[3]:
                low_stock.append(material)
        
        conn.close()
        return {"materials": materials, "low_stock_alerts": low_stock}
    
    def get_workers_status(self):
        """Статус рабочих"""
        conn = sqlite3.connect('construction.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT w.id, w.name, w.specialty, w.hourly_rate, w.phone, w.status, 
                   p.name as project_name
            FROM workers w
            LEFT JOIN projects p ON w.current_project_id = p.id
            ORDER BY w.specialty, w.name
        ''')
        
        workers = []
        for row in cursor.fetchall():
            workers.append({
                "id": row[0],
                "name": row[1],
                "specialty": row[2],
                "hourly_rate": row[3],
                "phone": row[4],
                "status": row[5],
                "current_project": row[6]
            })
        
        conn.close()
        return workers
    
    def get_urgent_tasks(self):
        """Срочные задачи"""
        conn = sqlite3.connect('construction.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.id, t.title, t.description, t.priority, t.due_date, t.status,
                   p.name as project_name, w.name as worker_name
            FROM tasks t
            JOIN projects p ON t.project_id = p.id
            LEFT JOIN workers w ON t.assigned_worker_id = w.id
            WHERE t.status != 'completed' AND t.due_date <= date('now', '+7 days')
            ORDER BY t.due_date ASC
        ''')
        
        urgent_tasks = []
        for row in cursor.fetchall():
            urgent_tasks.append({
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "priority": row[3],
                "due_date": row[4],
                "status": row[5],
                "project": row[6],
                "assigned_to": row[7]
            })
        
        conn.close()
        return urgent_tasks
    
    def calculate_project_costs(self, project_id):
        """Расчет затрат по проекту"""
        conn = sqlite3.connect('construction.db')
        cursor = conn.cursor()
        
        # Затраты на материалы (примерный расчет)
        cursor.execute("SELECT budget FROM projects WHERE id = ?", (project_id,))
        budget = cursor.fetchone()[0]
        
        # Затраты на рабочую силу
        cursor.execute('''
            SELECT SUM(w.hourly_rate * 8 * 30) as labor_cost
            FROM workers w
            WHERE w.current_project_id = ?
        ''', (project_id,))
        
        labor_cost = cursor.fetchone()[0] or 0
        
        # Примерные затраты на материалы (40% от бюджета)
        material_cost = budget * 0.4
        
        # Накладные расходы (15% от бюджета)
        overhead_cost = budget * 0.15
        
        conn.close()
        
        return {
            "budget": budget,
            "labor_cost": labor_cost,
            "material_cost": material_cost,
            "overhead_cost": overhead_cost,
            "total_estimated": labor_cost + material_cost + overhead_cost,
            "remaining_budget": budget - (labor_cost + material_cost + overhead_cost)
        }
    
    def create_project(self, project_data):
        """Создание нового проекта"""
        conn = sqlite3.connect('construction.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO projects (name, address, type, budget, start_date, end_date, manager_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            project_data['name'],
            project_data['address'],
            project_data['type'],
            project_data['budget'],
            project_data['start_date'],
            project_data['end_date'],
            project_data.get('manager_id', 1)
        ))
        
        project_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {"project_id": project_id, "message": "Проект создан успешно"}
    
    def assign_worker_to_project(self, worker_id, project_id):
        """Назначение рабочего на проект"""
        conn = sqlite3.connect('construction.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE workers SET current_project_id = ?, status = 'busy'
            WHERE id = ?
        ''', (project_id, worker_id))
        
        conn.commit()
        conn.close()
        
        return {"message": "Рабочий назначен на проект"}
    
    def update_project_progress(self, project_id, progress):
        """Обновление прогресса проекта"""
        conn = sqlite3.connect('construction.db')
        cursor = conn.cursor()
        
        status = "completed" if progress >= 100 else "active"
        
        cursor.execute('''
            UPDATE projects SET progress = ?, status = ?
            WHERE id = ?
        ''', (progress, status, project_id))
        
        conn.commit()
        conn.close()
        
        return {"message": f"Прогресс проекта обновлен до {progress}%"}
    
    def get_construction_dashboard(self):
        """Панель управления строительством"""
        projects = self.get_projects_overview()
        materials = self.get_materials_status()
        workers = self.get_workers_status()
        urgent_tasks = self.get_urgent_tasks()
        
        # Статистика
        active_projects = len([p for p in projects if p['status'] == 'active'])
        available_workers = len([w for w in workers if w['status'] == 'available'])
        low_stock_count = len(materials['low_stock_alerts'])
        
        return {
            "summary": {
                "total_projects": len(projects),
                "active_projects": active_projects,
                "total_workers": len(workers),
                "available_workers": available_workers,
                "low_stock_materials": low_stock_count,
                "urgent_tasks": len(urgent_tasks)
            },
            "projects": projects[:5],  # Последние 5 проектов
            "urgent_tasks": urgent_tasks,
            "low_stock_alerts": materials['low_stock_alerts'],
            "worker_summary": {
                "available": available_workers,
                "busy": len([w for w in workers if w['status'] == 'busy']),
                "total": len(workers)
            }
        }

# Глобальный экземпляр
construction_manager = ConstructionManagerAgent()