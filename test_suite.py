"""
Комплексный набор тестов для системы
"""
import unittest
import sqlite3
import os
import json
from datetime import datetime
from enhanced_security import enhanced_security

class TestEnhancedSecurity(unittest.TestCase):
    """Тесты системы безопасности"""
    
    def setUp(self):
        """Подготовка к тестам"""
        if os.path.exists('security.db'):
            os.remove('security.db')
        enhanced_security.setup_database()
    
    def test_password_hashing(self):
        """Тест хеширования паролей"""
        password = "test123"
        salt = "testsalt"
        hash1 = enhanced_security._hash_password(password, salt)
        hash2 = enhanced_security._hash_password(password, salt)
        self.assertEqual(hash1, hash2)
        
        # Разные соли должны давать разные хеши
        hash3 = enhanced_security._hash_password(password, "differentsalt")
        self.assertNotEqual(hash1, hash3)
    
    def test_authentication_success(self):
        """Тест успешной аутентификации"""
        result = enhanced_security.authenticate("director", "admin2024", "127.0.0.1", "TestAgent")
        self.assertTrue(result["success"])
        self.assertIn("session_token", result)
    
    def test_authentication_failure(self):
        """Тест неудачной аутентификации"""
        result = enhanced_security.authenticate("director", "wrongpassword", "127.0.0.1", "TestAgent")
        self.assertFalse(result["success"])
    
    def test_session_validation(self):
        """Тест валидации сессии"""
        auth_result = enhanced_security.authenticate("director", "admin2024", "127.0.0.1", "TestAgent")
        session_token = auth_result["session_token"]
        
        session_data = enhanced_security.validate_session(session_token)
        self.assertIsNotNone(session_data)
        self.assertEqual(session_data["username"], "director")
    
    def test_data_encryption(self):
        """Тест шифрования данных"""
        original_data = "Секретная информация"
        encrypted = enhanced_security.encrypt_data(original_data)
        decrypted = enhanced_security.decrypt_data(encrypted)
        
        self.assertNotEqual(original_data, encrypted)
        self.assertEqual(original_data, decrypted)
    
    def test_audit_logging(self):
        """Тест логирования аудита"""
        enhanced_security.log_audit(1, "test_action", "test_resource", "127.0.0.1", "TestAgent", True, "Test details")
        
        audit_log = enhanced_security.get_audit_log(1)
        self.assertEqual(len(audit_log), 1)
        self.assertEqual(audit_log[0]["action"], "test_action")

class TestSystemIntegration(unittest.TestCase):
    """Интеграционные тесты"""
    
    def test_database_creation(self):
        """Тест создания базы данных"""
        self.assertTrue(os.path.exists('security.db'))
        
        conn = sqlite3.connect('security.db')
        cursor = conn.cursor()
        
        # Проверка таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['users', 'audit_log', 'sessions']
        for table in expected_tables:
            self.assertIn(table, tables)
        
        conn.close()
    
    def test_default_admin_creation(self):
        """Тест создания администратора по умолчанию"""
        conn = sqlite3.connect('security.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT username, role FROM users WHERE username = 'director'")
        result = cursor.fetchone()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "director")
        self.assertEqual(result[1], "admin")
        
        conn.close()

class TestPerformance(unittest.TestCase):
    """Тесты производительности"""
    
    def test_authentication_performance(self):
        """Тест производительности аутентификации"""
        import time
        
        start_time = time.time()
        for i in range(10):
            enhanced_security.authenticate("director", "admin2024", "127.0.0.1", "TestAgent")
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 10
        self.assertLess(avg_time, 1.0)  # Менее 1 секунды на аутентификацию
    
    def test_encryption_performance(self):
        """Тест производительности шифрования"""
        import time
        
        data = "Test data for encryption" * 100
        
        start_time = time.time()
        for i in range(100):
            encrypted = enhanced_security.encrypt_data(data)
            enhanced_security.decrypt_data(encrypted)
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 100
        self.assertLess(avg_time, 0.1)  # Менее 0.1 секунды на операцию

def run_all_tests():
    """Запуск всех тестов"""
    print("🧪 Запуск комплексного тестирования...")
    print("=" * 50)
    
    # Создание тестового набора
    test_suite = unittest.TestSuite()
    
    # Добавление тестов безопасности
    test_suite.addTest(unittest.makeSuite(TestEnhancedSecurity))
    test_suite.addTest(unittest.makeSuite(TestSystemIntegration))
    test_suite.addTest(unittest.makeSuite(TestPerformance))
    
    # Запуск тестов
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Отчет о результатах
    print("\n" + "=" * 50)
    print(f"📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"✅ Пройдено: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Провалено: {len(result.failures)}")
    print(f"🚫 Ошибки: {len(result.errors)}")
    print(f"📈 Покрытие: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\n❌ ПРОВАЛИВШИЕСЯ ТЕСТЫ:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
    
    if result.errors:
        print("\n🚫 ОШИБКИ:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split('\\n')[-2]}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n🎉 Все тесты пройдены успешно!")
    else:
        print("\n⚠️ Некоторые тесты провалились. Требуется исправление.")
    
    input("\nНажмите Enter для завершения...")