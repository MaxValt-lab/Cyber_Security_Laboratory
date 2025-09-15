"""
Веб-интерфейс для строительной системы DevBuild
"""
from flask import Flask, render_template_string, request, jsonify
import sys
import os

# Добавление пути к агентам
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

try:
    from construction_manager_agent import construction_manager
    from project_analysis_agent import project_analysis_agent
    from procurement_agent import procurement_agent
except ImportError as e:
    print(f"Ошибка импорта агентов: {e}")

app = Flask(__name__)

# HTML шаблон
CONSTRUCTION_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>DevBuild - Строительная Система</title>
    <meta charset="utf-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white; min-height: 100vh;
        }
        .header { 
            background: rgba(0,0,0,0.3); padding: 20px; 
            border-bottom: 3px solid #f39c12;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .dashboard-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
            gap: 20px; margin-top: 20px;
        }
        .card { 
            background: rgba(255,255,255,0.1); 
            backdrop-filter: blur(10px);
            border-radius: 15px; padding: 25px; 
            border: 1px solid rgba(243,156,18,0.3);
            transition: transform 0.3s ease;
        }
        .card:hover { transform: translateY(-5px); }
        .card h3 { color: #f39c12; margin-bottom: 15px; font-size: 1.3em; }
        .btn { 
            background: linear-gradient(45deg, #f39c12, #e67e22);
            color: white; border: none; padding: 12px 24px;
            border-radius: 8px; cursor: pointer; font-weight: bold;
            margin: 5px; transition: all 0.3s ease;
        }
        .btn:hover { transform: scale(1.05); box-shadow: 0 5px 15px rgba(243,156,18,0.4); }
        .btn-success { background: linear-gradient(45deg, #27ae60, #2ecc71); }
        .btn-warning { background: linear-gradient(45deg, #e74c3c, #c0392b); }
        .metric-value { font-size: 2em; font-weight: bold; color: #f39c12; }
        .status-ok { color: #2ecc71; }
        .status-warning { color: #f39c12; }
        .status-error { color: #e74c3c; }
        .progress-bar { 
            background: rgba(255,255,255,0.2); height: 20px; border-radius: 10px; 
            overflow: hidden; margin: 10px 0;
        }
        .progress-fill { 
            background: linear-gradient(45deg, #f39c12, #e67e22); 
            height: 100%; transition: width 0.3s ease;
        }
        .data-table { 
            width: 100%; border-collapse: collapse; margin-top: 15px;
        }
        .data-table th, .data-table td { 
            padding: 10px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.2);
        }
        .data-table th { background: rgba(243,156,18,0.2); }
        .modal {
            display: none; position: fixed; z-index: 1000; left: 0; top: 0;
            width: 100%; height: 100%; background: rgba(0,0,0,0.7);
        }
        .modal-content {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            margin: 5% auto; padding: 30px; width: 80%; max-width: 800px;
            border-radius: 15px; border: 2px solid #f39c12; color: white;
        }
        .close { color: #f39c12; float: right; font-size: 28px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>🏗️ DevBuild - Строительная Система</h1>
            <p>Комплексное управление строительными проектами</p>
        </div>
    </div>

    <div class="container">
        <div class="dashboard-grid">
            <!-- Обзор проектов -->
            <div class="card">
                <h3>📊 Обзор Проектов</h3>
                <div id="projects-overview">
                    <div class="metric-value" id="total-projects">0</div>
                    <p>Всего проектов</p>
                    <div class="metric-value" id="active-projects">0</div>
                    <p>Активных проектов</p>
                </div>
                <button class="btn" onclick="loadProjects()">Показать Проекты</button>
                <button class="btn btn-success" onclick="showCreateProject()">Новый Проект</button>
            </div>

            <!-- Материалы и склад -->
            <div class="card">
                <h3>📦 Материалы и Склад</h3>
                <div id="materials-status">
                    <p>Загрузка данных...</p>
                </div>
                <button class="btn" onclick="loadMaterials()">Статус Склада</button>
                <button class="btn btn-warning" onclick="showLowStock()">Критические Остатки</button>
            </div>

            <!-- Рабочие и персонал -->
            <div class="card">
                <h3>👷 Рабочие и Персонал</h3>
                <div id="workers-status">
                    <div class="metric-value" id="available-workers">0</div>
                    <p>Доступных рабочих</p>
                    <div class="metric-value" id="busy-workers">0</div>
                    <p>Занятых рабочих</p>
                </div>
                <button class="btn" onclick="loadWorkers()">Управление Персоналом</button>
            </div>

            <!-- Закупки и поставщики -->
            <div class="card">
                <h3>🛒 Закупки и Поставщики</h3>
                <div id="procurement-status">
                    <div class="metric-value" id="pending-orders">0</div>
                    <p>Ожидающих заказов</p>
                    <div class="metric-value" id="open-tenders">0</div>
                    <p>Открытых тендеров</p>
                </div>
                <button class="btn" onclick="loadProcurement()">Управление Закупками</button>
                <button class="btn btn-success" onclick="showCreateOrder()">Новый Заказ</button>
            </div>

            <!-- Анализ документов -->
            <div class="card">
                <h3>📋 Анализ Документов</h3>
                <div id="analysis-status">
                    <p>Система анализа проектной документации</p>
                    <ul>
                        <li>✅ Проверка чертежей</li>
                        <li>✅ Анализ смет</li>
                        <li>✅ Валидация спецификаций</li>
                    </ul>
                </div>
                <button class="btn" onclick="showDocumentUpload()">Загрузить Документы</button>
                <button class="btn" onclick="showAnalysisReport()">Отчеты Анализа</button>
            </div>

            <!-- Срочные задачи -->
            <div class="card">
                <h3>⚡ Срочные Задачи</h3>
                <div id="urgent-tasks">
                    <p>Загрузка задач...</p>
                </div>
                <button class="btn btn-warning" onclick="loadUrgentTasks()">Обновить Задачи</button>
            </div>
        </div>
    </div>

    <!-- Модальные окна -->
    <div id="projectsModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('projectsModal')">&times;</span>
            <h2>📊 Проекты</h2>
            <div id="projects-list"></div>
        </div>
    </div>

    <div id="materialsModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('materialsModal')">&times;</span>
            <h2>📦 Материалы на Складе</h2>
            <div id="materials-list"></div>
        </div>
    </div>

    <div id="workersModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('workersModal')">&times;</span>
            <h2>👷 Персонал</h2>
            <div id="workers-list"></div>
        </div>
    </div>

    <script>
        // Загрузка данных при старте
        window.onload = function() {
            loadDashboardData();
        };

        function loadDashboardData() {
            // Загрузка основных метрик
            fetch('/api/dashboard')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('total-projects').textContent = data.summary.total_projects;
                    document.getElementById('active-projects').textContent = data.summary.active_projects;
                    document.getElementById('available-workers').textContent = data.worker_summary.available;
                    document.getElementById('busy-workers').textContent = data.worker_summary.busy;
                    document.getElementById('pending-orders').textContent = data.summary.pending_orders || 0;
                    document.getElementById('open-tenders').textContent = data.summary.open_tenders || 0;
                    
                    // Обновление срочных задач
                    updateUrgentTasks(data.urgent_tasks);
                    
                    // Обновление статуса материалов
                    updateMaterialsStatus(data.low_stock_alerts);
                });
        }

        function updateUrgentTasks(tasks) {
            const container = document.getElementById('urgent-tasks');
            if (tasks.length === 0) {
                container.innerHTML = '<p class="status-ok">✅ Нет срочных задач</p>';
                return;
            }
            
            let html = '';
            tasks.forEach(task => {
                const priority = task.priority === 'high' ? 'status-error' : 'status-warning';
                html += `<div class="${priority}">• ${task.title} (до ${task.due_date})</div>`;
            });
            container.innerHTML = html;
        }

        function updateMaterialsStatus(lowStock) {
            const container = document.getElementById('materials-status');
            if (lowStock.length === 0) {
                container.innerHTML = '<p class="status-ok">✅ Все материалы в наличии</p>';
            } else {
                container.innerHTML = `<p class="status-warning">⚠️ ${lowStock.length} материалов требуют пополнения</p>`;
            }
        }

        function loadProjects() {
            fetch('/api/projects')
                .then(r => r.json())
                .then(data => {
                    let html = '<table class="data-table"><tr><th>Название</th><th>Статус</th><th>Прогресс</th><th>Бюджет</th></tr>';
                    data.forEach(project => {
                        html += `<tr>
                            <td>${project.name}</td>
                            <td><span class="status-${project.status === 'active' ? 'ok' : 'warning'}">${project.status}</span></td>
                            <td>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: ${project.progress}%"></div>
                                </div>
                                ${project.progress}%
                            </td>
                            <td>₽${project.budget.toLocaleString()}</td>
                        </tr>`;
                    });
                    html += '</table>';
                    document.getElementById('projects-list').innerHTML = html;
                    document.getElementById('projectsModal').style.display = 'block';
                });
        }

        function loadMaterials() {
            fetch('/api/materials')
                .then(r => r.json())
                .then(data => {
                    let html = '<table class="data-table"><tr><th>Материал</th><th>Остаток</th><th>Мин. запас</th><th>Статус</th></tr>';
                    data.materials.forEach(material => {
                        const statusClass = material.status === 'ok' ? 'status-ok' : 'status-error';
                        html += `<tr>
                            <td>${material.name}</td>
                            <td>${material.stock} ${material.unit}</td>
                            <td>${material.min_stock} ${material.unit}</td>
                            <td><span class="${statusClass}">${material.status === 'ok' ? '✅ OK' : '⚠️ Мало'}</span></td>
                        </tr>`;
                    });
                    html += '</table>';
                    document.getElementById('materials-list').innerHTML = html;
                    document.getElementById('materialsModal').style.display = 'block';
                });
        }

        function loadWorkers() {
            fetch('/api/workers')
                .then(r => r.json())
                .then(data => {
                    let html = '<table class="data-table"><tr><th>Имя</th><th>Специальность</th><th>Статус</th><th>Проект</th></tr>';
                    data.forEach(worker => {
                        const statusClass = worker.status === 'available' ? 'status-ok' : 'status-warning';
                        html += `<tr>
                            <td>${worker.name}</td>
                            <td>${worker.specialty}</td>
                            <td><span class="${statusClass}">${worker.status === 'available' ? 'Доступен' : 'Занят'}</span></td>
                            <td>${worker.current_project || '-'}</td>
                        </tr>`;
                    });
                    html += '</table>';
                    document.getElementById('workers-list').innerHTML = html;
                    document.getElementById('workersModal').style.display = 'block';
                });
        }

        function loadProcurement() {
            alert('Открытие модуля закупок...');
        }

        function loadUrgentTasks() {
            loadDashboardData();
        }

        function showCreateProject() {
            alert('Форма создания нового проекта...');
        }

        function showCreateOrder() {
            alert('Форма создания заказа...');
        }

        function showLowStock() {
            fetch('/api/materials')
                .then(r => r.json())
                .then(data => {
                    if (data.low_stock_alerts.length === 0) {
                        alert('Все материалы в достаточном количестве');
                    } else {
                        let message = 'Материалы требующие пополнения:\\n\\n';
                        data.low_stock_alerts.forEach(item => {
                            message += `• ${item.name}: ${item.stock} ${item.unit} (мин: ${item.min_stock})\\n`;
                        });
                        alert(message);
                    }
                });
        }

        function showDocumentUpload() {
            alert('Модуль загрузки и анализа документов...');
        }

        function showAnalysisReport() {
            alert('Отчеты по анализу проектной документации...');
        }

        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }

        // Закрытие модального окна при клике вне его
        window.onclick = function(event) {
            if (event.target.classList.contains('modal')) {
                event.target.style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def construction_dashboard():
    return render_template_string(CONSTRUCTION_TEMPLATE)

@app.route('/api/dashboard')
def api_dashboard():
    try:
        dashboard_data = construction_manager.get_construction_dashboard()
        
        # Добавление данных о закупках
        procurement_data = procurement_agent.get_procurement_dashboard()
        dashboard_data['summary']['pending_orders'] = procurement_data['summary']['pending_orders']
        dashboard_data['summary']['open_tenders'] = procurement_data['summary']['open_tenders']
        
        return jsonify(dashboard_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/projects')
def api_projects():
    try:
        projects = construction_manager.get_projects_overview()
        return jsonify(projects)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/materials')
def api_materials():
    try:
        materials = construction_manager.get_materials_status()
        return jsonify(materials)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/workers')
def api_workers():
    try:
        workers = construction_manager.get_workers_status()
        return jsonify(workers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/procurement')
def api_procurement():
    try:
        procurement_data = procurement_agent.get_procurement_dashboard()
        return jsonify(procurement_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analysis/upload', methods=['POST'])
def api_upload_document():
    try:
        # Имитация загрузки документа
        project_id = request.form.get('project_id', 1)
        document_type = request.form.get('document_type', 'blueprint')
        
        # В реальной системе здесь была бы обработка файла
        result = {
            "message": "Документ загружен для анализа",
            "document_id": 123,
            "analysis_status": "pending"
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🏗️ Запуск строительной системы DevBuild...")
    print("📊 Веб-интерфейс: http://localhost:8091")
    print("🔧 Модули: Проекты, Материалы, Персонал, Закупки, Анализ документов")
    
    app.run(host='0.0.0.0', port=8091, debug=False)