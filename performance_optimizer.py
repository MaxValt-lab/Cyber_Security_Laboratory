"""
Оптимизатор производительности с кэшированием и оптимизацией БД
"""
import sqlite3
import json
import time
import threading
from datetime import datetime, timedelta
from functools import wraps
import hashlib

class PerformanceOptimizer:
    def __init__(self):
        self.cache = {}
        self.cache_stats = {"hits": 0, "misses": 0}
        self.query_stats = {}
        self.setup_optimization_db()
        
    def setup_optimization_db(self):
        """База данных для оптимизации"""
        conn = sqlite3.connect('performance.db')
        cursor = conn.cursor()
        
        # Таблица кэша
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cache_entries (
                key TEXT PRIMARY KEY,
                value TEXT,
                created_at TEXT,
                expires_at TEXT,
                access_count INTEGER DEFAULT 0
            )
        ''')
        
        # Таблица статистики запросов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS query_performance (
                id INTEGER PRIMARY KEY,
                query_hash TEXT,
                query_text TEXT,
                execution_time REAL,
                timestamp TEXT,
                result_count INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def cache_result(self, ttl=300):
        """Декоратор для кэширования результатов"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Создание ключа кэша
                cache_key = self._generate_cache_key(func.__name__, args, kwargs)
                
                # Проверка кэша
                cached_result = self.get_from_cache(cache_key)
                if cached_result is not None:
                    self.cache_stats["hits"] += 1
                    return cached_result
                
                # Выполнение функции
                self.cache_stats["misses"] += 1
                result = func(*args, **kwargs)
                
                # Сохранение в кэш
                self.set_cache(cache_key, result, ttl)
                
                return result
            return wrapper
        return decorator
    
    def _generate_cache_key(self, func_name, args, kwargs):
        """Генерация ключа кэша"""
        key_data = f"{func_name}:{str(args)}:{str(sorted(kwargs.items()))}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get_from_cache(self, key):
        """Получение из кэша"""
        # Проверка памяти
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() < entry["expires_at"]:
                entry["access_count"] += 1
                return entry["value"]
            else:
                del self.cache[key]
        
        # Проверка БД
        conn = sqlite3.connect('performance.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT value, expires_at, access_count FROM cache_entries 
            WHERE key = ? AND expires_at > datetime('now')
        ''', (key,))
        
        result = cursor.fetchone()
        if result:
            value, expires_at, access_count = result
            
            # Обновление счетчика
            cursor.execute('''
                UPDATE cache_entries SET access_count = access_count + 1 
                WHERE key = ?
            ''', (key,))
            
            # Загрузка в память
            self.cache[key] = {
                "value": json.loads(value),
                "expires_at": datetime.fromisoformat(expires_at),
                "access_count": access_count + 1
            }
            
            conn.commit()
            conn.close()
            return json.loads(value)
        
        conn.close()
        return None
    
    def set_cache(self, key, value, ttl):
        """Сохранение в кэш"""
        expires_at = datetime.now() + timedelta(seconds=ttl)
        
        # Сохранение в память
        self.cache[key] = {
            "value": value,
            "expires_at": expires_at,
            "access_count": 1
        }
        
        # Сохранение в БД
        conn = sqlite3.connect('performance.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO cache_entries (key, value, created_at, expires_at, access_count)
            VALUES (?, ?, ?, ?, 1)
        ''', (key, json.dumps(value), datetime.now().isoformat(), expires_at.isoformat()))
        
        conn.commit()
        conn.close()
    
    def optimize_database(self, db_path):
        """Оптимизация базы данных"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        optimizations = []
        
        # Анализ таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            
            # Создание индексов
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            for column in columns:
                column_name = column[1]
                if column_name.endswith('_id') or column_name in ['timestamp', 'created_at']:
                    index_name = f"idx_{table_name}_{column_name}"
                    try:
                        cursor.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({column_name})")
                        optimizations.append(f"Создан индекс: {index_name}")
                    except:
                        pass
        
        # VACUUM для дефрагментации
        cursor.execute("VACUUM")
        optimizations.append("Выполнена дефрагментация")
        
        # ANALYZE для обновления статистики
        cursor.execute("ANALYZE")
        optimizations.append("Обновлена статистика")
        
        conn.commit()
        conn.close()
        
        return optimizations
    
    def monitor_query_performance(self, query, params=None):
        """Мониторинг производительности запросов"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Логирование производительности
                query_hash = hashlib.md5(query.encode()).hexdigest()
                
                conn = sqlite3.connect('performance.db')
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO query_performance (query_hash, query_text, execution_time, timestamp, result_count)
                    VALUES (?, ?, ?, ?, ?)
                ''', (query_hash, query[:100], execution_time, datetime.now().isoformat(), 
                     len(result) if isinstance(result, list) else 1))
                
                conn.commit()
                conn.close()
                
                # Предупреждение о медленных запросах
                if execution_time > 1.0:
                    print(f"⚠️ Медленный запрос ({execution_time:.2f}s): {query[:50]}...")
                
                return result
            return wrapper
        return decorator
    
    def get_performance_stats(self):
        """Статистика производительности"""
        conn = sqlite3.connect('performance.db')
        cursor = conn.cursor()
        
        # Статистика кэша
        cache_hit_rate = 0
        if self.cache_stats["hits"] + self.cache_stats["misses"] > 0:
            cache_hit_rate = self.cache_stats["hits"] / (self.cache_stats["hits"] + self.cache_stats["misses"]) * 100
        
        # Медленные запросы
        cursor.execute('''
            SELECT query_text, AVG(execution_time), COUNT(*) 
            FROM query_performance 
            WHERE timestamp > datetime('now', '-24 hours')
            GROUP BY query_hash 
            ORDER BY AVG(execution_time) DESC 
            LIMIT 5
        ''')
        slow_queries = cursor.fetchall()
        
        # Размер кэша
        cursor.execute("SELECT COUNT(*) FROM cache_entries WHERE expires_at > datetime('now')")
        cache_size = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "cache_hit_rate": round(cache_hit_rate, 2),
            "cache_size": cache_size,
            "memory_cache_size": len(self.cache),
            "slow_queries": slow_queries,
            "total_queries": self.cache_stats["hits"] + self.cache_stats["misses"]
        }
    
    def cleanup_cache(self):
        """Очистка устаревшего кэша"""
        # Очистка памяти
        current_time = datetime.now()
        expired_keys = [key for key, entry in self.cache.items() 
                       if current_time >= entry["expires_at"]]
        
        for key in expired_keys:
            del self.cache[key]
        
        # Очистка БД
        conn = sqlite3.connect('performance.db')
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM cache_entries WHERE expires_at <= datetime('now')")
        deleted_count = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return {"memory_cleaned": len(expired_keys), "db_cleaned": deleted_count}
    
    def optimize_large_dataset_query(self, query, params, batch_size=1000):
        """Оптимизация запросов к большим данным"""
        results = []
        offset = 0
        
        while True:
            # Добавление LIMIT и OFFSET к запросу
            paginated_query = f"{query} LIMIT {batch_size} OFFSET {offset}"
            
            conn = sqlite3.connect('performance.db')
            cursor = conn.cursor()
            
            if params:
                cursor.execute(paginated_query, params)
            else:
                cursor.execute(paginated_query)
            
            batch_results = cursor.fetchall()
            conn.close()
            
            if not batch_results:
                break
            
            results.extend(batch_results)
            offset += batch_size
            
            # Предотвращение блокировки
            time.sleep(0.001)
        
        return results

# Глобальный экземпляр
performance_optimizer = PerformanceOptimizer()

# Примеры использования декораторов
@performance_optimizer.cache_result(ttl=600)
def get_analytics_data():
    """Пример кэшированной функции аналитики"""
    # Имитация тяжелых вычислений
    time.sleep(0.1)
    return {
        "total_projects": 25,
        "active_users": 12,
        "revenue": 2500000,
        "timestamp": datetime.now().isoformat()
    }

@performance_optimizer.monitor_query_performance("SELECT * FROM users")
def get_users():
    """Пример мониторинга запроса"""
    # Имитация запроса к БД
    return [{"id": 1, "name": "User1"}, {"id": 2, "name": "User2"}]