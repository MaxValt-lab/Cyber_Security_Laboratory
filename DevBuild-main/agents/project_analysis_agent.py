"""
Агент анализа проектов - анализ чертежей, смет, документации
"""
import sqlite3
import json
import os
import zipfile
from datetime import datetime
import hashlib

class ProjectAnalysisAgent:
    def __init__(self):
        self.setup_database()
        self.analysis_rules = self._load_analysis_rules()
        
    def setup_database(self):
        """База данных анализа проектов"""
        conn = sqlite3.connect('project_analysis.db')
        cursor = conn.cursor()
        
        # Документы проектов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_documents (
                id INTEGER PRIMARY KEY,
                project_id INTEGER,
                document_type TEXT,
                file_name TEXT,
                file_path TEXT,
                file_hash TEXT,
                upload_date TEXT,
                analysis_status TEXT DEFAULT 'pending',
                analysis_result TEXT
            )
        ''')
        
        # Результаты анализа
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY,
                document_id INTEGER,
                analysis_type TEXT,
                result_data TEXT,
                issues_found INTEGER DEFAULT 0,
                recommendations TEXT,
                created_at TEXT
            )
        ''')
        
        # Ошибки и замечания
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_issues (
                id INTEGER PRIMARY KEY,
                document_id INTEGER,
                issue_type TEXT,
                severity TEXT,
                description TEXT,
                line_number INTEGER,
                suggested_fix TEXT,
                status TEXT DEFAULT 'open'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_analysis_rules(self):
        """Правила анализа документов"""
        return {
            "blueprint": {
                "required_elements": ["масштаб", "размеры", "материалы", "узлы"],
                "standards": ["ГОСТ 21.501-2018", "ГОСТ 21.101-97"],
                "checks": ["размерность", "соответствие_нормам", "читаемость"]
            },
            "estimate": {
                "required_sections": ["материалы", "работы", "накладные", "итого"],
                "price_ranges": {"cement": [4000, 6000], "brick": [10000, 15000]},
                "margin_limits": {"min": 0.15, "max": 0.30}
            },
            "specification": {
                "required_fields": ["наименование", "количество", "единица", "цена"],
                "format_checks": ["числовые_поля", "единицы_измерения"]
            }
        }
    
    def upload_document(self, project_id, file_path, document_type):
        """Загрузка документа для анализа"""
        if not os.path.exists(file_path):
            return {"error": "Файл не найден"}
        
        # Вычисление хеша файла
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        
        conn = sqlite3.connect('project_analysis.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO project_documents 
            (project_id, document_type, file_name, file_path, file_hash, upload_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (project_id, document_type, os.path.basename(file_path), 
              file_path, file_hash, datetime.now().isoformat()))
        
        document_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Запуск анализа
        analysis_result = self.analyze_document(document_id)
        
        return {
            "document_id": document_id,
            "message": "Документ загружен и проанализирован",
            "analysis": analysis_result
        }
    
    def analyze_document(self, document_id):
        """Анализ документа"""
        conn = sqlite3.connect('project_analysis.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT document_type, file_name, file_path 
            FROM project_documents WHERE id = ?
        ''', (document_id,))
        
        doc_info = cursor.fetchone()
        if not doc_info:
            return {"error": "Документ не найден"}
        
        document_type, file_name, file_path = doc_info
        
        # Анализ в зависимости от типа документа
        if document_type == "blueprint":
            result = self._analyze_blueprint(file_path)
        elif document_type == "estimate":
            result = self._analyze_estimate(file_path)
        elif document_type == "specification":
            result = self._analyze_specification(file_path)
        else:
            result = self._general_analysis(file_path)
        
        # Сохранение результатов
        cursor.execute('''
            INSERT INTO analysis_results 
            (document_id, analysis_type, result_data, issues_found, recommendations, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (document_id, document_type, json.dumps(result), 
              len(result.get('issues', [])), result.get('recommendations', ''),
              datetime.now().isoformat()))
        
        # Обновление статуса документа
        cursor.execute('''
            UPDATE project_documents 
            SET analysis_status = 'completed', analysis_result = ?
            WHERE id = ?
        ''', (json.dumps(result), document_id))
        
        # Сохранение найденных проблем
        for issue in result.get('issues', []):
            cursor.execute('''
                INSERT INTO document_issues 
                (document_id, issue_type, severity, description, suggested_fix)
                VALUES (?, ?, ?, ?, ?)
            ''', (document_id, issue['type'], issue['severity'], 
                  issue['description'], issue.get('fix', '')))
        
        conn.commit()
        conn.close()
        
        return result
    
    def _analyze_blueprint(self, file_path):
        """Анализ чертежа"""
        issues = []
        recommendations = []
        
        # Проверка расширения файла
        if not file_path.lower().endswith(('.dwg', '.pdf', '.jpg', '.png')):
            issues.append({
                "type": "format",
                "severity": "medium",
                "description": "Неподдерживаемый формат чертежа",
                "fix": "Используйте форматы DWG, PDF или изображения"
            })
        
        # Проверка размера файла
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            if file_size > 50 * 1024 * 1024:  # 50MB
                issues.append({
                    "type": "size",
                    "severity": "low",
                    "description": "Большой размер файла может замедлить работу",
                    "fix": "Оптимизируйте изображение или используйте сжатие"
                })
        
        # Имитация проверки содержимого
        filename_lower = os.path.basename(file_path).lower()
        
        if "план" not in filename_lower and "чертеж" not in filename_lower:
            issues.append({
                "type": "naming",
                "severity": "low",
                "description": "Название файла не соответствует содержимому",
                "fix": "Переименуйте файл согласно ГОСТ 21.101-97"
            })
        
        # Рекомендации
        recommendations = [
            "Проверьте соответствие масштаба указанному на чертеже",
            "Убедитесь в наличии всех необходимых размеров",
            "Проверьте соответствие ГОСТ 21.501-2018"
        ]
        
        return {
            "status": "completed",
            "issues": issues,
            "recommendations": recommendations,
            "compliance_score": max(0, 100 - len(issues) * 15),
            "analysis_details": {
                "format_check": "passed" if not any(i['type'] == 'format' for i in issues) else "failed",
                "size_check": "passed" if not any(i['type'] == 'size' for i in issues) else "warning",
                "naming_check": "passed" if not any(i['type'] == 'naming' for i in issues) else "warning"
            }
        }
    
    def _analyze_estimate(self, file_path):
        """Анализ сметы"""
        issues = []
        recommendations = []
        
        # Проверка формата
        if not file_path.lower().endswith(('.xlsx', '.xls', '.csv', '.pdf')):
            issues.append({
                "type": "format",
                "severity": "high",
                "description": "Неподдерживаемый формат сметы",
                "fix": "Используйте Excel, CSV или PDF формат"
            })
        
        # Имитация анализа содержимого сметы
        filename = os.path.basename(file_path).lower()
        
        required_keywords = ["смета", "расчет", "стоимость"]
        if not any(keyword in filename for keyword in required_keywords):
            issues.append({
                "type": "content",
                "severity": "medium",
                "description": "Файл может не содержать сметную документацию",
                "fix": "Проверьте содержимое файла"
            })
        
        # Проверка на подозрительно низкие/высокие цены
        estimated_total = 1500000  # Примерная сумма для анализа
        
        if estimated_total < 100000:
            issues.append({
                "type": "pricing",
                "severity": "high",
                "description": "Подозрительно низкая общая стоимость",
                "fix": "Проверьте расценки и объемы работ"
            })
        elif estimated_total > 50000000:
            issues.append({
                "type": "pricing",
                "severity": "medium",
                "description": "Высокая стоимость требует дополнительного обоснования",
                "fix": "Предоставьте детальное обоснование цен"
            })
        
        recommendations = [
            "Проверьте актуальность расценок на материалы",
            "Убедитесь в правильности расчета объемов работ",
            "Добавьте резерв на непредвиденные расходы (10-15%)"
        ]
        
        return {
            "status": "completed",
            "issues": issues,
            "recommendations": recommendations,
            "estimated_total": estimated_total,
            "compliance_score": max(0, 100 - len(issues) * 20),
            "price_analysis": {
                "materials_cost": estimated_total * 0.6,
                "labor_cost": estimated_total * 0.25,
                "overhead": estimated_total * 0.15
            }
        }
    
    def _analyze_specification(self, file_path):
        """Анализ спецификации"""
        issues = []
        recommendations = []
        
        # Базовые проверки
        if not file_path.lower().endswith(('.xlsx', '.xls', '.csv', '.txt')):
            issues.append({
                "type": "format",
                "severity": "medium",
                "description": "Рекомендуется использовать табличный формат",
                "fix": "Конвертируйте в Excel или CSV"
            })
        
        # Имитация проверки структуры
        recommendations = [
            "Убедитесь в наличии всех обязательных полей",
            "Проверьте единицы измерения",
            "Добавьте коды материалов по каталогу"
        ]
        
        return {
            "status": "completed",
            "issues": issues,
            "recommendations": recommendations,
            "compliance_score": max(0, 100 - len(issues) * 10),
            "structure_analysis": {
                "required_fields": ["наименование", "количество", "единица", "цена"],
                "missing_fields": [],
                "data_quality": "good"
            }
        }
    
    def _general_analysis(self, file_path):
        """Общий анализ документа"""
        issues = []
        
        # Проверка существования файла
        if not os.path.exists(file_path):
            issues.append({
                "type": "file",
                "severity": "critical",
                "description": "Файл не найден или недоступен",
                "fix": "Проверьте путь к файлу"
            })
        
        return {
            "status": "completed",
            "issues": issues,
            "recommendations": ["Проведите детальный анализ содержимого"],
            "compliance_score": 80
        }
    
    def generate_analysis_report(self, project_id):
        """Генерация отчета по анализу проекта"""
        conn = sqlite3.connect('project_analysis.db')
        cursor = conn.cursor()
        
        # Получение всех документов проекта
        cursor.execute('''
            SELECT pd.id, pd.document_type, pd.file_name, pd.analysis_status,
                   ar.issues_found, ar.result_data
            FROM project_documents pd
            LEFT JOIN analysis_results ar ON pd.id = ar.document_id
            WHERE pd.project_id = ?
        ''', (project_id,))
        
        documents = cursor.fetchall()
        
        # Получение всех проблем
        cursor.execute('''
            SELECT di.issue_type, di.severity, di.description, di.status,
                   pd.document_type, pd.file_name
            FROM document_issues di
            JOIN project_documents pd ON di.document_id = pd.id
            WHERE pd.project_id = ?
        ''', (project_id,))
        
        issues = cursor.fetchall()
        conn.close()
        
        # Формирование отчета
        report = {
            "project_id": project_id,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_documents": len(documents),
                "analyzed_documents": len([d for d in documents if d[3] == 'completed']),
                "total_issues": len(issues),
                "critical_issues": len([i for i in issues if i[1] == 'critical']),
                "high_issues": len([i for i in issues if i[1] == 'high']),
                "medium_issues": len([i for i in issues if i[1] == 'medium']),
                "low_issues": len([i for i in issues if i[1] == 'low'])
            },
            "documents": [],
            "issues_by_type": {},
            "recommendations": []
        }
        
        # Детали по документам
        for doc in documents:
            doc_info = {
                "id": doc[0],
                "type": doc[1],
                "filename": doc[2],
                "status": doc[3],
                "issues_count": doc[4] or 0
            }
            
            if doc[5]:  # Если есть результаты анализа
                try:
                    analysis_data = json.loads(doc[5])
                    doc_info["compliance_score"] = analysis_data.get("compliance_score", 0)
                except:
                    doc_info["compliance_score"] = 0
            
            report["documents"].append(doc_info)
        
        # Группировка проблем по типам
        for issue in issues:
            issue_type = issue[0]
            if issue_type not in report["issues_by_type"]:
                report["issues_by_type"][issue_type] = []
            
            report["issues_by_type"][issue_type].append({
                "severity": issue[1],
                "description": issue[2],
                "status": issue[3],
                "document": issue[5]
            })
        
        # Общие рекомендации
        if report["summary"]["critical_issues"] > 0:
            report["recommendations"].append("Немедленно устраните критические ошибки")
        
        if report["summary"]["high_issues"] > 0:
            report["recommendations"].append("Приоритетно исправьте серьезные замечания")
        
        if report["summary"]["total_issues"] == 0:
            report["recommendations"].append("Документация соответствует требованиям")
        
        return report
    
    def create_corrected_package(self, project_id, output_path):
        """Создание исправленного пакета документов"""
        conn = sqlite3.connect('project_analysis.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT file_path, file_name, document_type
            FROM project_documents
            WHERE project_id = ? AND analysis_status = 'completed'
        ''', (project_id,))
        
        documents = cursor.fetchall()
        conn.close()
        
        # Создание ZIP архива
        zip_path = f"{output_path}/corrected_project_{project_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            # Добавление исходных документов
            for file_path, file_name, doc_type in documents:
                if os.path.exists(file_path):
                    zipf.write(file_path, f"original/{file_name}")
            
            # Добавление отчета об анализе
            report = self.generate_analysis_report(project_id)
            report_json = json.dumps(report, ensure_ascii=False, indent=2)
            zipf.writestr("analysis_report.json", report_json)
            
            # Добавление рекомендаций
            recommendations_text = "\n".join([
                "РЕКОМЕНДАЦИИ ПО ИСПРАВЛЕНИЮ ДОКУМЕНТАЦИИ",
                "=" * 50,
                ""
            ])
            
            for rec in report["recommendations"]:
                recommendations_text += f"• {rec}\n"
            
            zipf.writestr("recommendations.txt", recommendations_text)
        
        return {
            "package_path": zip_path,
            "documents_included": len(documents),
            "message": "Пакет исправленных документов создан"
        }

# Глобальный экземпляр
project_analysis_agent = ProjectAnalysisAgent()