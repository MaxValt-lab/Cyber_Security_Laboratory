"""
Агент закупок - управление поставщиками, заказами, тендерами
"""
import sqlite3
import json
from datetime import datetime, timedelta

class ProcurementAgent:
    def __init__(self):
        self.setup_database()
        
    def setup_database(self):
        """База данных закупок"""
        conn = sqlite3.connect('procurement.db')
        cursor = conn.cursor()
        
        # Поставщики
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                contact_person TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                rating REAL DEFAULT 5.0,
                reliability_score INTEGER DEFAULT 100,
                payment_terms TEXT,
                delivery_time INTEGER DEFAULT 7
            )
        ''')
        
        # Заказы
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchase_orders (
                id INTEGER PRIMARY KEY,
                supplier_id INTEGER,
                project_id INTEGER,
                order_date TEXT,
                delivery_date TEXT,
                status TEXT DEFAULT 'pending',
                total_amount REAL,
                payment_status TEXT DEFAULT 'unpaid',
                notes TEXT
            )
        ''')
        
        # Позиции заказов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY,
                order_id INTEGER,
                material_name TEXT,
                quantity REAL,
                unit TEXT,
                unit_price REAL,
                total_price REAL,
                delivery_status TEXT DEFAULT 'pending'
            )
        ''')
        
        # Тендеры
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tenders (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                project_id INTEGER,
                start_date TEXT,
                end_date TEXT,
                status TEXT DEFAULT 'open',
                budget_limit REAL,
                requirements TEXT
            )
        ''')
        
        # Предложения по тендерам
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tender_bids (
                id INTEGER PRIMARY KEY,
                tender_id INTEGER,
                supplier_id INTEGER,
                bid_amount REAL,
                delivery_time INTEGER,
                bid_date TEXT,
                proposal_details TEXT,
                status TEXT DEFAULT 'submitted'
            )
        ''')
        
        conn.commit()
        conn.close()
        
        self._add_sample_data()
    
    def _add_sample_data(self):
        """Добавление тестовых данных"""
        conn = sqlite3.connect('procurement.db')
        cursor = conn.cursor()
        
        # Проверка существования данных
        cursor.execute("SELECT COUNT(*) FROM suppliers")
        if cursor.fetchone()[0] == 0:
            # Поставщики
            suppliers = [
                ("СтройМатериалы ООО", "Иванов И.И.", "+7-495-123-45-67", "info@stroymaterials.ru", "г. Москва, ул. Строительная, 15", 4.5, 95, "30 дней", 5),
                ("КирпичЗавод", "Петров П.П.", "+7-495-234-56-78", "sales@kirpich.ru", "г. Подольск, пр. Заводской, 22", 4.8, 98, "14 дней", 3),
                ("МеталлТорг", "Сидоров С.С.", "+7-495-345-67-89", "order@metall.ru", "г. Люберцы, ул. Металлургов, 8", 4.2, 88, "45 дней", 7),
                ("ПескоГрав", "Козлов К.К.", "+7-495-456-78-90", "info@peskograv.ru", "г. Раменское, ул. Карьерная, 5", 4.6, 92, "предоплата", 2),
                ("ИнструментСервис", "Новиков Н.Н.", "+7-495-567-89-01", "tools@service.ru", "г. Москва, ул. Инструментальная, 12", 4.3, 90, "21 день", 4)
            ]
            
            cursor.executemany('''
                INSERT INTO suppliers (name, contact_person, phone, email, address, rating, reliability_score, payment_terms, delivery_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', suppliers)
            
            # Заказы
            orders = [
                (1, 1, "2024-01-10", "2024-01-15", "delivered", 225000, "paid", "Доставка выполнена в срок"),
                (2, 1, "2024-01-12", "2024-01-15", "delivered", 300000, "paid", "Качество материалов отличное"),
                (3, 2, "2024-01-15", "2024-01-22", "in_transit", 675000, "partial", "Частичная предоплата внесена"),
                (1, 2, "2024-01-18", "2024-01-23", "pending", 180000, "unpaid", "Ожидается подтверждение заказа")
            ]
            
            cursor.executemany('''
                INSERT INTO purchase_orders (supplier_id, project_id, order_date, delivery_date, status, total_amount, payment_status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', orders)
            
            # Позиции заказов
            order_items = [
                (1, "Цемент М400", 50, "тонна", 4500, 225000, "delivered"),
                (2, "Кирпич красный", 25, "тыс.шт", 12000, 300000, "delivered"),
                (3, "Арматура 12мм", 15, "тонна", 45000, 675000, "in_transit"),
                (4, "Песок речной", 30, "м³", 800, 24000, "pending"),
                (4, "Щебень 20-40", 20, "м³", 1200, 24000, "pending")
            ]
            
            cursor.executemany('''
                INSERT INTO order_items (order_id, material_name, quantity, unit, unit_price, total_price, delivery_status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', order_items)
            
            # Тендеры
            tenders = [
                ("Поставка строительных материалов для ЖК Солнечный", "Требуется поставка цемента, кирпича и арматуры", 2, "2024-01-20", "2024-01-30", "open", 2000000, "Сертификаты качества обязательны"),
                ("Аренда строительной техники", "Аренда экскаватора и автокрана на 3 месяца", 1, "2024-01-15", "2024-01-25", "evaluation", 500000, "Опыт работы не менее 5 лет")
            ]
            
            cursor.executemany('''
                INSERT INTO tenders (title, description, project_id, start_date, end_date, status, budget_limit, requirements)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', tenders)
            
            # Предложения по тендерам
            bids = [
                (1, 1, 1800000, 10, "2024-01-22", "Предлагаем качественные материалы с доставкой", "submitted"),
                (1, 2, 1750000, 7, "2024-01-23", "Лучшие цены и быстрая доставка", "submitted"),
                (2, 5, 450000, 14, "2024-01-18", "Современная техника, опытные операторы", "submitted")
            ]
            
            cursor.executemany('''
                INSERT INTO tender_bids (tender_id, supplier_id, bid_amount, delivery_time, bid_date, proposal_details, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', bids)
        
        conn.commit()
        conn.close()
    
    def get_suppliers_list(self):
        """Список поставщиков"""
        conn = sqlite3.connect('procurement.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, contact_person, phone, email, rating, reliability_score, 
                   payment_terms, delivery_time
            FROM suppliers ORDER BY rating DESC
        ''')
        
        suppliers = []
        for row in cursor.fetchall():
            suppliers.append({
                "id": row[0],
                "name": row[1],
                "contact_person": row[2],
                "phone": row[3],
                "email": row[4],
                "rating": row[5],
                "reliability_score": row[6],
                "payment_terms": row[7],
                "delivery_time": row[8]
            })
        
        conn.close()
        return suppliers
    
    def create_purchase_order(self, order_data):
        """Создание заказа на закупку"""
        conn = sqlite3.connect('procurement.db')
        cursor = conn.cursor()
        
        # Создание заказа
        cursor.execute('''
            INSERT INTO purchase_orders 
            (supplier_id, project_id, order_date, delivery_date, total_amount, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            order_data['supplier_id'],
            order_data['project_id'],
            datetime.now().isoformat(),
            order_data['delivery_date'],
            order_data['total_amount'],
            order_data.get('notes', '')
        ))
        
        order_id = cursor.lastrowid
        
        # Добавление позиций заказа
        for item in order_data['items']:
            cursor.execute('''
                INSERT INTO order_items 
                (order_id, material_name, quantity, unit, unit_price, total_price)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                order_id,
                item['material_name'],
                item['quantity'],
                item['unit'],
                item['unit_price'],
                item['quantity'] * item['unit_price']
            ))
        
        conn.commit()
        conn.close()
        
        return {"order_id": order_id, "message": "Заказ создан успешно"}
    
    def get_orders_status(self):
        """Статус заказов"""
        conn = sqlite3.connect('procurement.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT po.id, s.name, po.order_date, po.delivery_date, po.status, 
                   po.total_amount, po.payment_status
            FROM purchase_orders po
            JOIN suppliers s ON po.supplier_id = s.id
            ORDER BY po.order_date DESC
        ''')
        
        orders = []
        for row in cursor.fetchall():
            orders.append({
                "id": row[0],
                "supplier": row[1],
                "order_date": row[2],
                "delivery_date": row[3],
                "status": row[4],
                "total_amount": row[5],
                "payment_status": row[6]
            })
        
        conn.close()
        return orders
    
    def create_tender(self, tender_data):
        """Создание тендера"""
        conn = sqlite3.connect('procurement.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tenders 
            (title, description, project_id, start_date, end_date, budget_limit, requirements)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            tender_data['title'],
            tender_data['description'],
            tender_data['project_id'],
            tender_data['start_date'],
            tender_data['end_date'],
            tender_data['budget_limit'],
            tender_data['requirements']
        ))
        
        tender_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {"tender_id": tender_id, "message": "Тендер создан успешно"}
    
    def get_active_tenders(self):
        """Активные тендеры"""
        conn = sqlite3.connect('procurement.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, description, start_date, end_date, status, budget_limit
            FROM tenders 
            WHERE status IN ('open', 'evaluation')
            ORDER BY end_date ASC
        ''')
        
        tenders = []
        for row in cursor.fetchall():
            # Получение количества предложений
            cursor.execute("SELECT COUNT(*) FROM tender_bids WHERE tender_id = ?", (row[0],))
            bids_count = cursor.fetchone()[0]
            
            tenders.append({
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "start_date": row[3],
                "end_date": row[4],
                "status": row[5],
                "budget_limit": row[6],
                "bids_count": bids_count
            })
        
        conn.close()
        return tenders
    
    def evaluate_tender_bids(self, tender_id):
        """Оценка предложений по тендеру"""
        conn = sqlite3.connect('procurement.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT tb.id, s.name, tb.bid_amount, tb.delivery_time, tb.bid_date,
                   s.rating, s.reliability_score, tb.proposal_details
            FROM tender_bids tb
            JOIN suppliers s ON tb.supplier_id = s.id
            WHERE tb.tender_id = ?
            ORDER BY tb.bid_amount ASC
        ''', (tender_id,))
        
        bids = []
        for row in cursor.fetchall():
            # Расчет общего балла
            price_score = max(0, 100 - (row[2] / 1000000 * 10))  # Чем меньше цена, тем выше балл
            delivery_score = max(0, 100 - row[3] * 2)  # Чем быстрее доставка, тем выше балл
            supplier_score = (row[5] * 10 + row[6]) / 2  # Рейтинг и надежность
            
            total_score = (price_score * 0.4 + delivery_score * 0.3 + supplier_score * 0.3)
            
            bids.append({
                "id": row[0],
                "supplier": row[1],
                "bid_amount": row[2],
                "delivery_time": row[3],
                "bid_date": row[4],
                "supplier_rating": row[5],
                "reliability_score": row[6],
                "proposal_details": row[7],
                "total_score": round(total_score, 2),
                "recommendation": "Рекомендуется" if total_score >= 80 else "Требует анализа" if total_score >= 60 else "Не рекомендуется"
            })
        
        # Сортировка по общему баллу
        bids.sort(key=lambda x: x['total_score'], reverse=True)
        
        conn.close()
        return bids
    
    def get_supplier_performance(self, supplier_id):
        """Анализ работы поставщика"""
        conn = sqlite3.connect('procurement.db')
        cursor = conn.cursor()
        
        # Основная информация о поставщике
        cursor.execute('''
            SELECT name, rating, reliability_score, payment_terms, delivery_time
            FROM suppliers WHERE id = ?
        ''', (supplier_id,))
        
        supplier_info = cursor.fetchone()
        
        # Статистика заказов
        cursor.execute('''
            SELECT COUNT(*) as total_orders,
                   SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) as completed_orders,
                   SUM(total_amount) as total_value,
                   AVG(total_amount) as avg_order_value
            FROM purchase_orders WHERE supplier_id = ?
        ''', (supplier_id,))
        
        order_stats = cursor.fetchone()
        
        # Последние заказы
        cursor.execute('''
            SELECT order_date, delivery_date, status, total_amount, payment_status
            FROM purchase_orders 
            WHERE supplier_id = ?
            ORDER BY order_date DESC LIMIT 5
        ''', (supplier_id,))
        
        recent_orders = cursor.fetchall()
        
        conn.close()
        
        if not supplier_info:
            return {"error": "Поставщик не найден"}
        
        # Расчет показателей
        completion_rate = 0
        if order_stats[0] > 0:
            completion_rate = (order_stats[1] / order_stats[0]) * 100
        
        return {
            "supplier_info": {
                "name": supplier_info[0],
                "rating": supplier_info[1],
                "reliability_score": supplier_info[2],
                "payment_terms": supplier_info[3],
                "delivery_time": supplier_info[4]
            },
            "performance_metrics": {
                "total_orders": order_stats[0],
                "completed_orders": order_stats[1],
                "completion_rate": round(completion_rate, 2),
                "total_value": order_stats[2] or 0,
                "avg_order_value": order_stats[3] or 0
            },
            "recent_orders": [
                {
                    "order_date": order[0],
                    "delivery_date": order[1],
                    "status": order[2],
                    "amount": order[3],
                    "payment_status": order[4]
                } for order in recent_orders
            ]
        }
    
    def get_procurement_dashboard(self):
        """Панель управления закупками"""
        conn = sqlite3.connect('procurement.db')
        cursor = conn.cursor()
        
        # Общая статистика
        cursor.execute("SELECT COUNT(*) FROM suppliers")
        total_suppliers = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM purchase_orders WHERE status = 'pending'")
        pending_orders = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tenders WHERE status = 'open'")
        open_tenders = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT SUM(total_amount) FROM purchase_orders 
            WHERE order_date >= date('now', '-30 days')
        ''')
        monthly_spending = cursor.fetchone()[0] or 0
        
        # Топ поставщики
        cursor.execute('''
            SELECT s.name, s.rating, COUNT(po.id) as orders_count,
                   SUM(po.total_amount) as total_value
            FROM suppliers s
            LEFT JOIN purchase_orders po ON s.id = po.supplier_id
            GROUP BY s.id, s.name, s.rating
            ORDER BY s.rating DESC, total_value DESC
            LIMIT 5
        ''')
        
        top_suppliers = []
        for row in cursor.fetchall():
            top_suppliers.append({
                "name": row[0],
                "rating": row[1],
                "orders_count": row[2],
                "total_value": row[3] or 0
            })
        
        # Срочные заказы
        cursor.execute('''
            SELECT po.id, s.name, po.delivery_date, po.total_amount, po.status
            FROM purchase_orders po
            JOIN suppliers s ON po.supplier_id = s.id
            WHERE po.delivery_date <= date('now', '+7 days') AND po.status != 'delivered'
            ORDER BY po.delivery_date ASC
        ''')
        
        urgent_orders = []
        for row in cursor.fetchall():
            urgent_orders.append({
                "id": row[0],
                "supplier": row[1],
                "delivery_date": row[2],
                "amount": row[3],
                "status": row[4]
            })
        
        conn.close()
        
        return {
            "summary": {
                "total_suppliers": total_suppliers,
                "pending_orders": pending_orders,
                "open_tenders": open_tenders,
                "monthly_spending": monthly_spending
            },
            "top_suppliers": top_suppliers,
            "urgent_orders": urgent_orders,
            "recommendations": [
                "Проверьте срочные заказы на этой неделе",
                "Оцените предложения по открытым тендерам",
                "Обновите рейтинги поставщиков"
            ]
        }

# Глобальный экземпляр
procurement_agent = ProcurementAgent()