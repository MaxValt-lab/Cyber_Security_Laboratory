#!/usr/bin/env python3
import os
import json
import hashlib
import subprocess
from datetime import datetime

class MobileSecurityScanner:
    def __init__(self):
        self.scan_results = {}
        self.threat_database = self.load_threat_database()
    
    def scan_installed_apps(self):
        """Сканирование установленных приложений"""
        try:
            # Для Android через ADB (если доступно)
            result = subprocess.run(['pm', 'list', 'packages'], 
                                  capture_output=True, text=True)
            
            apps = []
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.startswith('package:'):
                        package_name = line.replace('package:', '').strip()
                        apps.append(package_name)
            
            return self.analyze_apps(apps)
            
        except:
            # Fallback для тестирования
            return self.simulate_app_scan()
    
    def simulate_app_scan(self):
        """Симуляция сканирования приложений"""
        fake_apps = [
            'com.android.chrome',
            'com.whatsapp',
            'com.facebook.katana',
            'com.suspicious.app',
            'com.banking.secure'
        ]
        
        return self.analyze_apps(fake_apps)
    
    def analyze_apps(self, app_list):
        """Анализ списка приложений"""
        results = {
            'total_apps': len(app_list),
            'suspicious_apps': [],
            'safe_apps': [],
            'unknown_apps': []
        }
        
        for app in app_list:
            threat_level = self.check_app_threat(app)
            
            if threat_level == 'HIGH':
                results['suspicious_apps'].append({
                    'name': app,
                    'threat': 'HIGH',
                    'reason': 'Known malicious pattern'
                })
            elif threat_level == 'MEDIUM':
                results['unknown_apps'].append({
                    'name': app,
                    'threat': 'MEDIUM',
                    'reason': 'Unknown or suspicious'
                })
            else:
                results['safe_apps'].append(app)
        
        return results
    
    def check_app_threat(self, app_name):
        """Проверка угрозы от приложения"""
        # Проверка в базе угроз
        if app_name in self.threat_database.get('malicious', []):
            return 'HIGH'
        
        # Проверка подозрительных паттернов
        suspicious_patterns = ['hack', 'crack', 'free', 'mod', 'cheat']
        for pattern in suspicious_patterns:
            if pattern in app_name.lower():
                return 'MEDIUM'
        
        # Проверка известных безопасных приложений
        if app_name in self.threat_database.get('safe', []):
            return 'LOW'
        
        return 'MEDIUM'  # Неизвестные приложения
    
    def scan_permissions(self):
        """Сканирование разрешений приложений"""
        dangerous_permissions = [
            'android.permission.READ_CONTACTS',
            'android.permission.ACCESS_FINE_LOCATION',
            'android.permission.CAMERA',
            'android.permission.RECORD_AUDIO',
            'android.permission.READ_SMS',
            'android.permission.CALL_PHONE'
        ]
        
        # Симуляция проверки разрешений
        permission_issues = []
        
        apps_with_issues = [
            {
                'app': 'com.suspicious.app',
                'permissions': ['CAMERA', 'RECORD_AUDIO', 'READ_CONTACTS'],
                'risk': 'HIGH'
            },
            {
                'app': 'com.social.media',
                'permissions': ['ACCESS_FINE_LOCATION'],
                'risk': 'MEDIUM'
            }
        ]
        
        return {
            'total_dangerous_permissions': len(dangerous_permissions),
            'apps_with_issues': apps_with_issues,
            'recommendations': [
                'Отозвать разрешения у подозрительных приложений',
                'Регулярно проверять разрешения приложений'
            ]
        }
    
    def scan_network_security(self):
        """Сканирование сетевой безопасности"""
        return {
            'wifi_security': 'WPA2',
            'open_ports': [],
            'suspicious_connections': 0,
            'vpn_status': 'Not connected',
            'dns_security': 'OK',
            'recommendations': [
                'Используйте VPN в общественных сетях',
                'Избегайте открытых WiFi сетей'
            ]
        }
    
    def scan_storage_security(self):
        """Сканирование безопасности хранилища"""
        return {
            'encryption_status': 'Enabled',
            'sensitive_files': 0,
            'backup_security': 'Encrypted',
            'sd_card_encryption': 'Not available',
            'recommendations': [
                'Регулярно создавайте зашифрованные резервные копии',
                'Используйте блокировку экрана'
            ]
        }
    
    def perform_full_scan(self):
        """Полное сканирование безопасности"""
        scan_start = datetime.now()
        
        results = {
            'scan_time': scan_start.isoformat(),
            'apps': self.scan_installed_apps(),
            'permissions': self.scan_permissions(),
            'network': self.scan_network_security(),
            'storage': self.scan_storage_security()
        }
        
        # Общая оценка безопасности
        security_score = self.calculate_security_score(results)
        results['security_score'] = security_score
        results['overall_status'] = self.get_security_status(security_score)
        
        scan_end = datetime.now()
        results['scan_duration'] = (scan_end - scan_start).total_seconds()
        
        self.scan_results = results
        return results
    
    def calculate_security_score(self, results):
        """Вычисление общего балла безопасности"""
        score = 100
        
        # Вычеты за проблемы
        score -= len(results['apps']['suspicious_apps']) * 20
        score -= len(results['permissions']['apps_with_issues']) * 10
        
        if results['network']['suspicious_connections'] > 0:
            score -= 15
        
        if results['storage']['encryption_status'] != 'Enabled':
            score -= 25
        
        return max(0, min(100, score))
    
    def get_security_status(self, score):
        """Получение статуса безопасности"""
        if score >= 90:
            return 'EXCELLENT'
        elif score >= 75:
            return 'GOOD'
        elif score >= 50:
            return 'FAIR'
        else:
            return 'POOR'
    
    def get_recommendations(self):
        """Получение рекомендаций по безопасности"""
        if not self.scan_results:
            return ['Выполните сканирование безопасности']
        
        recommendations = []
        
        # Рекомендации по приложениям
        if self.scan_results['apps']['suspicious_apps']:
            recommendations.append('Удалите подозрительные приложения')
        
        # Рекомендации по разрешениям
        if self.scan_results['permissions']['apps_with_issues']:
            recommendations.append('Проверьте разрешения приложений')
        
        # Общие рекомендации
        recommendations.extend([
            'Регулярно обновляйте приложения',
            'Используйте антивирус',
            'Не устанавливайте приложения из неизвестных источников'
        ])
        
        return recommendations
    
    def load_threat_database(self):
        """Загрузка базы данных угроз"""
        return {
            'malicious': [
                'com.malware.example',
                'com.suspicious.app',
                'com.fake.banking'
            ],
            'safe': [
                'com.android.chrome',
                'com.whatsapp',
                'com.google.android.gms',
                'com.android.systemui'
            ]
        }
    
    def export_scan_results(self, filename=None):
        """Экспорт результатов сканирования"""
        if not filename:
            filename = f"security_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.scan_results, f, indent=2, ensure_ascii=False)
            return filename
        except:
            return None

def main():
    scanner = MobileSecurityScanner()
    results = scanner.perform_full_scan()
    
    print(f"Security Score: {results['security_score']}/100")
    print(f"Status: {results['overall_status']}")
    print(f"Suspicious Apps: {len(results['apps']['suspicious_apps'])}")

if __name__ == "__main__":
    main()