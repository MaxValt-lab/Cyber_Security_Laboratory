"""
Полный запуск улучшенной системы
"""
import os
import sys
import time
import threading
import subprocess
from datetime import datetime

# Импорт всех модулей системы
try:
    from advanced_security import advanced_security
    from performance_optimizer import performance_optimizer
    from mobile_interface import mobile_interface, notification_manager
    from enhanced_api_docs import APIDocumentationGenerator
except ImportError as e:
    print(f"⚠️ Ошибка импорта модуля: {e}")
    print("Некоторые функции могут быть недоступны")

class SystemLauncher:
    def __init__(self):
        self.services = {}
        self.system_status = "initializing"
        
    def initialize_system(self):
        """Инициализация всей системы"""
        print("🚀 Инициализация улучшенной системы управления...")
        print("=" * 60)
        
        # 1. Проверка зависимостей
        print("📦 Проверка зависимостей...")
        self._check_dependencies()
        
        # 2. Создание директорий
        print("📁 Создание рабочих директорий...")
        self._create_directories()
        
        # 3. Инициализация безопасности
        print("🔒 Инициализация системы безопасности...")
        self._init_security()
        
        # 4. Настройка производительности
        print("⚡ Настройка оптимизации производительности...")
        self._init_performance()
        
        # 5. Запуск мобильного интерфейса
        print("📱 Инициализация мобильного интерфейса...")
        self._init_mobile_interface()
        
        # 6. Генерация документации
        print("📚 Генерация API документации...")
        self._generate_documentation()
        
        # 7. Запуск основного сервера
        print("🌐 Запуск веб-сервера...")
        self._start_web_server()
        
        # 8. Запуск мониторинга
        print("📊 Запуск системы мониторинга...")
        self._start_monitoring()
        
        self.system_status = "running"
        print("\n✅ Система успешно запущена!")
        self._display_system_info()
        
    def _check_dependencies(self):
        """Проверка зависимостей"""
        required_modules = [
            'sqlite3', 'json', 'datetime', 'threading', 
            'hashlib', 'time', 'os', 'base64'
        ]
        
        optional_modules = [
            ('cryptography', 'Шифрование данных'),
            ('psutil', 'Мониторинг системы'),
            ('pyotp', 'Двухфакторная аутентификация'),
            ('qrcode', 'Генерация QR кодов')
        ]
        
        missing_optional = []
        for module, description in optional_modules:
            try:
                __import__(module)
                print(f"  ✅ {module} - {description}")
            except ImportError:
                missing_optional.append((module, description))
                print(f"  ⚠️ {module} - {description} (не установлен)")
        
        if missing_optional:
            print(f"\n💡 Для полной функциональности установите:")
            for module, desc in missing_optional:
                print(f"   pip install {module}")
    
    def _create_directories(self):
        """Создание рабочих директорий"""
        directories = [
            'backups', 'logs', 'docs', 'docs/api', 
            'cache', 'uploads', 'reports'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"  📁 {directory}")
    
    def _init_security(self):
        """Инициализация безопасности"""
        try:
            # Настройка 2FA для администратора
            setup_result = advanced_security.setup_2fa(1, "director")
            print(f"  🔐 2FA настроен (секрет: {setup_result['secret'][:8]}...)")
            
            # Создание зашифрованного бэкапа
            backup_files = ['security.db', 'advanced_security.db']
            backup_result = advanced_security.create_encrypted_backup(backup_files)
            print(f"  💾 Создан зашифрованный бэкап: {backup_result['size']} байт")
            
        except Exception as e:
            print(f"  ⚠️ Ошибка инициализации безопасности: {e}")
    
    def _init_performance(self):
        """Инициализация оптимизации производительности"""
        try:
            # Оптимизация баз данных
            databases = ['security.db', 'advanced_security.db', 'performance.db']
            for db in databases:
                if os.path.exists(db):
                    optimizations = performance_optimizer.optimize_database(db)
                    print(f"  ⚡ Оптимизирована БД {db}: {len(optimizations)} улучшений")
            
            # Очистка кэша
            cleanup_result = performance_optimizer.cleanup_cache()
            print(f"  🧹 Очищен кэш: {cleanup_result['memory_cleaned']} записей")
            
        except Exception as e:
            print(f"  ⚠️ Ошибка инициализации производительности: {e}")
    
    def _init_mobile_interface(self):
        """Инициализация мобильного интерфейса"""
        try:
            # Регистрация тестового устройства
            mobile_interface.register_mobile_device(1, "test_device_token", "Web", "1.0.0")
            
            # Отправка приветственного уведомления
            notification_manager.trigger_alert(
                "system_info", 
                "Система управления директора успешно запущена", 
                user_id=1
            )
            
            print(f"  📱 Мобильный интерфейс активен")
            
        except Exception as e:
            print(f"  ⚠️ Ошибка инициализации мобильного интерфейса: {e}")
    
    def _generate_documentation(self):
        """Генерация документации"""
        try:
            doc_generator = APIDocumentationGenerator()
            doc_generator.save_documentation()
            print(f"  📚 API документация создана")
            
        except Exception as e:
            print(f"  ⚠️ Ошибка генерации документации: {e}")
    
    def _start_web_server(self):
        """Запуск веб-сервера"""
        try:
            def run_server():
                subprocess.run([sys.executable, "simple_director_server.py"])
            
            server_thread = threading.Thread(target=run_server, daemon=True)
            server_thread.start()
            
            # Ожидание запуска сервера
            time.sleep(2)
            print(f"  🌐 Веб-сервер запущен на порту 8089")
            
        except Exception as e:
            print(f"  ⚠️ Ошибка запуска веб-сервера: {e}")
    
    def _start_monitoring(self):
        """Запуск мониторинга"""
        def monitoring_loop():
            while True:
                try:
                    # Сбор метрик производительности
                    stats = performance_optimizer.get_performance_stats()
                    
                    # Проверка безопасности
                    security_dashboard = advanced_security.get_security_dashboard()
                    
                    # Логирование критических событий
                    if stats['cache_hit_rate'] < 50:
                        notification_manager.trigger_alert(
                            "system_info",
                            f"Низкий процент попаданий в кэш: {stats['cache_hit_rate']}%"
                        )
                    
                    if security_dashboard['recent_alerts'] > 10:
                        notification_manager.trigger_alert(
                            "security_alert",
                            f"Высокое количество предупреждений безопасности: {security_dashboard['recent_alerts']}"
                        )
                    
                    time.sleep(60)  # Проверка каждую минуту
                    
                except Exception as e:
                    print(f"Ошибка мониторинга: {e}")
                    time.sleep(60)
        
        monitoring_thread = threading.Thread(target=monitoring_loop, daemon=True)
        monitoring_thread.start()
        print(f"  📊 Мониторинг активен")
    
    def _display_system_info(self):
        """Отображение информации о системе"""
        print("\n" + "=" * 60)
        print("🎉 СИСТЕМА УПРАВЛЕНИЯ ДИРЕКТОРА ЗАПУЩЕНА")
        print("=" * 60)
        print(f"🌐 Веб-интерфейс:     http://localhost:8089")
        print(f"🔐 Учетные данные:   director / admin2024")
        print(f"📱 Мобильный API:    http://localhost:8089/api/mobile/")
        print(f"📚 Документация:     docs/api/openapi.json")
        print(f"📊 Мониторинг:       logs/")
        print(f"💾 Резервные копии:  backups/")
        print(f"⚡ Кэш:              cache/")
        print("=" * 60)
        
        print("\n🔧 ДОСТУПНЫЕ ФУНКЦИИ:")
        print("✅ Двухфакторная аутентификация")
        print("✅ Зашифрованные резервные копии")
        print("✅ Оптимизация производительности")
        print("✅ Мобильные уведомления")
        print("✅ Детекция подозрительной активности")
        print("✅ Автоматический мониторинг")
        print("✅ Кэширование данных")
        print("✅ API документация")
        
        print("\n📈 СТАТУС СИСТЕМЫ:")
        try:
            perf_stats = performance_optimizer.get_performance_stats()
            print(f"   Процент попаданий в кэш: {perf_stats['cache_hit_rate']}%")
            print(f"   Размер кэша: {perf_stats['cache_size']} записей")
            
            security_stats = advanced_security.get_security_dashboard()
            print(f"   Уровень безопасности: {security_stats['security_level']}")
            print(f"   Пользователей с 2FA: {security_stats['users_with_2fa']}")
            
        except Exception as e:
            print(f"   ⚠️ Ошибка получения статистики: {e}")
        
        print(f"\n⏰ Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
    
    def run_interactive_menu(self):
        """Интерактивное меню управления"""
        while True:
            print("\n🎛️ ПАНЕЛЬ УПРАВЛЕНИЯ СИСТЕМОЙ")
            print("1. 📊 Показать статистику")
            print("2. 🔒 Статус безопасности")
            print("3. ⚡ Производительность")
            print("4. 📱 Мобильные уведомления")
            print("5. 💾 Создать резервную копию")
            print("6. 🧹 Очистить кэш")
            print("7. 📚 Обновить документацию")
            print("0. 🚪 Выход")
            
            choice = input("\nВыберите действие: ").strip()
            
            if choice == "1":
                self._show_statistics()
            elif choice == "2":
                self._show_security_status()
            elif choice == "3":
                self._show_performance_stats()
            elif choice == "4":
                self._send_test_notification()
            elif choice == "5":
                self._create_backup()
            elif choice == "6":
                self._cleanup_cache()
            elif choice == "7":
                self._update_documentation()
            elif choice == "0":
                print("👋 Завершение работы...")
                break
            else:
                print("❌ Неверный выбор")
    
    def _show_statistics(self):
        """Показать статистику"""
        try:
            stats = performance_optimizer.get_performance_stats()
            print(f"\n📊 СТАТИСТИКА ПРОИЗВОДИТЕЛЬНОСТИ:")
            print(f"   Процент попаданий в кэш: {stats['cache_hit_rate']}%")
            print(f"   Размер кэша: {stats['cache_size']} записей")
            print(f"   Всего запросов: {stats['total_queries']}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    def _show_security_status(self):
        """Показать статус безопасности"""
        try:
            security_stats = advanced_security.get_security_dashboard()
            print(f"\n🔒 СТАТУС БЕЗОПАСНОСТИ:")
            print(f"   Уровень безопасности: {security_stats['security_level']}")
            print(f"   Недавние предупреждения: {security_stats['recent_alerts']}")
            print(f"   Пользователей с 2FA: {security_stats['users_with_2fa']}")
            print(f"   Последний бэкап: {security_stats['last_backup'] or 'Не создан'}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    def _show_performance_stats(self):
        """Показать статистику производительности"""
        try:
            stats = performance_optimizer.get_performance_stats()
            print(f"\n⚡ ПРОИЗВОДИТЕЛЬНОСТЬ:")
            for query_info in stats['slow_queries'][:3]:
                print(f"   Медленный запрос: {query_info[0][:50]}... ({query_info[1]:.3f}s)")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    def _send_test_notification(self):
        """Отправить тестовое уведомление"""
        try:
            notification_manager.trigger_alert(
                "system_info",
                "Тестовое уведомление из панели управления",
                user_id=1
            )
            print("✅ Тестовое уведомление отправлено")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    def _create_backup(self):
        """Создать резервную копию"""
        try:
            backup_files = ['security.db', 'advanced_security.db', 'performance.db', 'mobile.db']
            result = advanced_security.create_encrypted_backup(backup_files)
            print(f"✅ Резервная копия создана: {result['backup_path']}")
            print(f"   Размер: {result['size']} байт")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    def _cleanup_cache(self):
        """Очистить кэш"""
        try:
            result = performance_optimizer.cleanup_cache()
            print(f"✅ Кэш очищен:")
            print(f"   Из памяти: {result['memory_cleaned']} записей")
            print(f"   Из БД: {result['db_cleaned']} записей")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    def _update_documentation(self):
        """Обновить документацию"""
        try:
            doc_generator = APIDocumentationGenerator()
            doc_generator.save_documentation()
            print("✅ Документация обновлена")
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    launcher = SystemLauncher()
    
    try:
        # Инициализация системы
        launcher.initialize_system()
        
        # Запуск интерактивного меню
        launcher.run_interactive_menu()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Система остановлена пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
    finally:
        print("👋 Завершение работы системы...")