"""
Веб-интерфейс генерального директора
"""
from flask import Flask, render_template_string, request, jsonify, session
import sqlite3
import json
import os
from datetime import datetime
from security_core import security_core

app = Flask(__name__)
app.secret_key = security_core.master_key

# HTML шаблон страницы входа
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Вход Генерального Директора</title>
    <meta charset="utf-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white; height: 100vh; display: flex; align-items: center; justify-content: center;
        }
        .login-container {
            background: rgba(255,255,255,0.1); backdrop-filter: blur(15px);
            border-radius: 20px; padding: 40px; width: 400px;
            border: 2px solid rgba(255,215,0,0.3); text-align: center;
        }
        .logo { font-size: 4em; margin-bottom: 20px; }
        h1 { color: #ffd700; margin-bottom: 30px; }
        .form-group { margin: 20px 0; text-align: left; }
        .form-group label { display: block; margin-bottom: 8px; color: #ffd700; }
        .form-group input {
            width: 100%; padding: 15px; border-radius: 10px;
            border: 1px solid #ffd700; background: rgba(255,255,255,0.1);
            color: white; font-size: 16px;
        }
        .form-group input::placeholder { color: rgba(255,255,255,0.7); }
        .login-btn {
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            color: #1e3c72; border: none; padding: 15px 40px;
            border-radius: 10px; cursor: pointer; font-weight: bold;
            font-size: 16px; width: 100%; margin-top: 20px;
            transition: all 0.3s ease;
        }
        .login-btn:hover { transform: scale(1.05); box-shadow: 0 5px 20px rgba(255,215,0,0.4); }
        .error { color: #ff4757; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">👑</div>
        <h1>Вход Директора</h1>
        
        <form onsubmit="login(event)">
            <div class="form-group">
                <label>Логин:</label>
                <input type="text" id="username" placeholder="Введите логин" required>
            </div>
            
            <div class="form-group">
                <label>Пароль:</label>
                <input type="password" id="password" placeholder="Введите пароль" required>
            </div>
            
            <button type="submit" class="login-btn">Войти в Систему</button>
        </form>
        
        <div id="error" class="error"></div>
        
        <p style="margin-top: 30px; font-size: 12px; opacity: 0.7;">
            Тестовые данные: director / admin2024
        </p>
    </div>

    <script>
        function login(event) {
            event.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            fetch('/api/director-login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, password})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    document.getElementById('error').textContent = data.error;
                }
            });
        }
    </script>
</body>
</html>
"""

# HTML шаблон главной страницы
DIRECTOR_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Панель Генерального Директора</title>
    <meta charset="utf-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white; min-height: 100vh;
        }
        .header { 
            background: rgba(0,0,0,0.2); padding: 20px; 
            border-bottom: 2px solid #ffd700;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .dashboard-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 20px; margin-top: 20px;
        }
        .card { 
            background: rgba(255,255,255,0.1); 
            backdrop-filter: blur(10px);
            border-radius: 15px; padding: 25px; 
            border: 1px solid rgba(255,215,0,0.3);
            transition: transform 0.3s ease;
        }
        .card:hover { transform: translateY(-5px); }
        .card h3 { color: #ffd700; margin-bottom: 15px; font-size: 1.3em; }
        .btn { 
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            color: #1e3c72; border: none; padding: 12px 24px;
            border-radius: 8px; cursor: pointer; font-weight: bold;
            margin: 5px; transition: all 0.3s ease;
        }
        .btn:hover { transform: scale(1.05); box-shadow: 0 5px 15px rgba(255,215,0,0.4); }
        .btn-danger { background: linear-gradient(45deg, #ff4757, #ff6b7a); color: white; }
        .status-indicator { 
            display: inline-block; width: 12px; height: 12px; 
            border-radius: 50%; margin-right: 8px;
        }
        .status-ok { background: #2ed573; }
        .status-error { background: #ff4757; }
        .metric-value { font-size: 2em; font-weight: bold; color: #ffd700; }
        .chat-btn { 
            position: fixed; bottom: 30px; right: 30px;
            width: 60px; height: 60px; border-radius: 50%;
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            border: none; cursor: pointer; font-size: 24px;
            box-shadow: 0 5px 20px rgba(255,215,0,0.4);
        }
        .modal {
            display: none; position: fixed; z-index: 1000; left: 0; top: 0;
            width: 100%; height: 100%; background: rgba(0,0,0,0.5);
        }
        .modal-content {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            margin: 10% auto; padding: 30px; width: 500px; border-radius: 15px;
            border: 2px solid #ffd700; color: white;
        }
        .close { color: #ffd700; float: right; font-size: 28px; cursor: pointer; }
        .form-group { margin: 15px 0; }
        .form-group label { display: block; margin-bottom: 5px; color: #ffd700; }
        .form-group select, .form-group input {
            width: 100%; padding: 10px; border-radius: 8px;
            border: 1px solid #ffd700; background: rgba(255,255,255,0.1);
            color: white;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>👑 Панель Генерального Директора</h1>
            <p>Добро пожаловать в систему управления</p>
            <button class="btn" onclick="logout()" style="float: right; margin-top: -40px;">Выйти</button>
        </div>
    </div>

    <div class="container">
        <div class="dashboard-grid">
            <div class="card">
                <h3>📊 Системные Метрики</h3>
                <div id="system-metrics">
                    <p>CPU: <span class="metric-value" id="cpu">--</span>%</p>
                    <p>Память: <span class="metric-value" id="memory">--</span>%</p>
                    <p>Диск: <span class="metric-value" id="disk">--</span>%</p>
                </div>
                <button class="btn" onclick="refreshMetrics()">Обновить</button>
            </div>

            <div class="card">
                <h3>🔧 Управление Сервисами</h3>
                <div id="services-status"></div>
                <button class="btn" onclick="restartAllServices()">Перезапустить Все</button>
                <button class="btn btn-danger" onclick="emergencyStop()">Аварийная Остановка</button>
            </div>

            <div class="card">
                <h3>💼 Управление Проектами</h3>
                <button class="btn" onclick="openProjectManager()">Менеджер Проектов</button>
                <button class="btn" onclick="openFinanceManager()">Финансы</button>
                <button class="btn" onclick="openHRManager()">Кадры</button>
            </div>

            <div class="card">
                <h3>📈 Аналитика</h3>
                <div class="metric-value" id="active-projects">0</div>
                <p>Активных проектов</p>
                <div class="metric-value" id="total-revenue">₽0</div>
                <p>Общая выручка</p>
                <button class="btn" onclick="generateReport()">Создать Отчет</button>
            </div>

            <div class="card">
                <h3>🔒 Безопасность</h3>
                <div id="security-status">
                    <p><span class="status-indicator status-ok"></span>Система защищена</p>
                    <p>Последний бэкап: <span id="last-backup">--</span></p>
                </div>
                <button class="btn" onclick="createBackup()">Создать Бэкап</button>
                <button class="btn" onclick="viewAuditLog()">Журнал Аудита</button>
            </div>

            <div class="card">
                <h3>👥 Команда</h3>
                <div id="team-status">
                    <p>Онлайн сотрудников: <span class="metric-value" id="online-staff">0</span></p>
                    <p>Активных задач: <span class="metric-value" id="active-tasks">0</span></p>
                </div>
                <button class="btn" onclick="viewTeamDashboard()">Панель Команды</button>
                <button class="btn" onclick="assignAgentToStaff()">Назначить Агента</button>
            </div>
        </div>
    </div>

    <button class="chat-btn" onclick="openChat()" title="Открыть чат с агентами">💬</button>

    <!-- Modal for Agent Assignment -->
    <div id="assignModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <h2>🤖 Назначение Агента Персоналу</h2>
            
            <div class="form-group">
                <label>Сотрудник:</label>
                <select id="staff-select">
                    <option value="">Загрузка...</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Агент:</label>
                <select id="agent-select-modal">
                    <option value="">Выберите агента</option>
                    <option value="construction">🏗️ Строительный Менеджер</option>
                    <option value="accounting">💰 Бухгалтерский Агент</option>
                    <option value="hr">👥 HR Агент</option>
                    <option value="analytics">📊 Аналитический Агент</option>
                    <option value="security">🔒 Агент Безопасности</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Уровень доступа:</label>
                <select id="permissions">
                    <option value="read">Чтение</option>
                    <option value="write">Чтение + Запись</option>
                    <option value="admin">Полный доступ</option>
                </select>
            </div>
            
            <button class="btn" onclick="performAssignment()">Назначить Агента</button>
        </div>
    </div>

    <script>
        function refreshMetrics() {
            fetch('/api/metrics')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('cpu').textContent = data.cpu || '--';
                    document.getElementById('memory').textContent = data.memory || '--';
                    document.getElementById('disk').textContent = data.disk || '--';
                    updateServicesStatus(data.services || {});
                });
        }

        function updateServicesStatus(services) {
            let html = '';
            for (let service in services) {
                let status = services[service];
                let indicator = status.healthy ? 'status-ok' : 'status-error';
                html += `<p><span class="status-indicator ${indicator}"></span>${service}</p>`;
            }
            document.getElementById('services-status').innerHTML = html;
        }

        function restartAllServices() {
            if (confirm('Перезапустить все сервисы?')) {
                fetch('/api/restart-services', {method: 'POST'})
                    .then(r => r.json())
                    .then(data => alert(data.message));
            }
        }

        function emergencyStop() {
            if (confirm('Выполнить аварийную остановку системы?')) {
                fetch('/api/emergency-stop', {method: 'POST'})
                    .then(r => r.json())
                    .then(data => alert(data.message));
            }
        }

        function createBackup() {
            fetch('/api/backup', {method: 'POST'})
                .then(r => r.json())
                .then(data => {
                    alert(data.message);
                    document.getElementById('last-backup').textContent = new Date().toLocaleString();
                });
        }

        function openChat() {
            window.open('/chat', 'chat', 'width=800,height=600');
        }

        function openProjectManager() { alert('Открытие менеджера проектов...'); }
        function openFinanceManager() { alert('Открытие финансового модуля...'); }
        function openHRManager() { alert('Открытие HR модуля...'); }
        function generateReport() { alert('Генерация отчета...'); }
        function viewAuditLog() { alert('Просмотр журнала аудита...'); }
        function viewTeamDashboard() { alert('Открытие панели команды...'); }
        
        function assignAgentToStaff() {
            document.getElementById('assignModal').style.display = 'block';
            loadStaffList();
        }
        
        function closeModal() {
            document.getElementById('assignModal').style.display = 'none';
        }
        
        function loadStaffList() {
            fetch('/api/staff-list')
                .then(r => r.json())
                .then(data => {
                    const select = document.getElementById('staff-select');
                    select.innerHTML = '<option value="">Выберите сотрудника</option>';
                    data.staff.forEach(person => {
                        select.innerHTML += `<option value="${person.id}">${person.name} - ${person.position}</option>`;
                    });
                });
        }
        
        function performAssignment() {
            const staffId = document.getElementById('staff-select').value;
            const agentType = document.getElementById('agent-select-modal').value;
            const permissions = document.getElementById('permissions').value;
            
            if (!staffId || !agentType) {
                alert('Выберите сотрудника и агента');
                return;
            }
            
            fetch('/api/assign-agent', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    staff_id: staffId,
                    agent_type: agentType,
                    permissions: permissions
                })
            })
            .then(r => r.json())
            .then(data => {
                alert(data.message);
                closeModal();
            });
        }

        function logout() {
            if (confirm('Выйти из системы?')) {
                fetch('/api/logout', {method: 'POST'})
                    .then(() => window.location.reload());
            }
        }
        
        // Auto-refresh every 30 seconds
        setInterval(refreshMetrics, 30000);
        refreshMetrics();
    </script>
</body>
</html>
"""

# HTML шаблон чата
CHAT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Чат с Агентами</title>
    <meta charset="utf-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white; height: 100vh; display: flex; flex-direction: column;
        }
        .chat-header { 
            background: rgba(0,0,0,0.2); padding: 15px; 
            border-bottom: 2px solid #ffd700; display: flex; align-items: center; gap: 15px;
        }
        .agent-selector { 
            background: rgba(255,255,255,0.1); border: 1px solid #ffd700;
            color: white; padding: 8px 15px; border-radius: 8px;
        }
        .chat-container { flex: 1; display: flex; flex-direction: column; padding: 20px; }
        .messages { 
            flex: 1; overflow-y: auto; background: rgba(255,255,255,0.05);
            border-radius: 15px; padding: 20px; margin-bottom: 20px;
            border: 1px solid rgba(255,215,0,0.2);
        }
        .message { 
            margin: 10px 0; padding: 12px 18px; border-radius: 18px; 
            max-width: 70%; word-wrap: break-word;
        }
        .message.user { 
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            color: #1e3c72; margin-left: auto; text-align: right;
        }
        .message.agent { 
            background: rgba(255,255,255,0.1); 
            border: 1px solid rgba(255,215,0,0.3);
        }
        .message-input { 
            display: flex; gap: 10px; background: rgba(255,255,255,0.1);
            padding: 15px; border-radius: 15px; border: 1px solid rgba(255,215,0,0.3);
        }
        .message-input input { 
            flex: 1; background: transparent; border: none; 
            color: white; padding: 12px; font-size: 16px;
        }
        .message-input input::placeholder { color: rgba(255,255,255,0.7); }
        .send-btn { 
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            color: #1e3c72; border: none; padding: 12px 20px;
            border-radius: 8px; cursor: pointer; font-weight: bold;
        }
        .agent-info { 
            background: rgba(255,215,0,0.1); padding: 10px; 
            border-radius: 8px; margin-bottom: 15px; font-size: 14px;
        }
        .load-chat-btn { 
            background: rgba(255,255,255,0.1); color: #ffd700;
            border: 1px solid #ffd700; padding: 8px 15px;
            border-radius: 8px; cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="chat-header">
        <h2>💬 Чат с Агентами</h2>
        <select class="agent-selector" id="agent-select" onchange="selectAgent()">
            <option value="">Выберите агента</option>
            <option value="construction">🏗️ Строительный Менеджер</option>
            <option value="accounting">💰 Бухгалтерский Агент</option>
            <option value="hr">👥 HR Агент</option>
            <option value="analytics">📊 Аналитический Агент</option>
            <option value="security">🔒 Агент Безопасности</option>
        </select>
        <button class="load-chat-btn" onclick="loadChatHistory()">📂 Загрузить Чат</button>
    </div>

    <div class="chat-container">
        <div class="agent-info" id="agent-info" style="display: none;">
            <strong id="agent-name">Агент</strong>: <span id="agent-description">Описание агента</span>
        </div>

        <div class="messages" id="messages">
            <div class="message agent">
                <strong>Система:</strong> Добро пожаловать! Выберите агента для начала общения.
            </div>
        </div>

        <div class="message-input">
            <input type="text" id="message-input" placeholder="Введите сообщение..." onkeypress="handleKeyPress(event)">
            <button class="send-btn" onclick="sendMessage()">Отправить</button>
        </div>
    </div>

    <script>
        let currentAgent = '';
        let chatHistory = [];

        const agentInfo = {
            'construction': {
                name: '🏗️ Строительный Менеджер',
                description: 'Управление проектами, материалами, рабочими и строительными процессами'
            },
            'accounting': {
                name: '💰 Бухгалтерский Агент', 
                description: 'Финансовый учет, отчетность, бюджетирование и налоговое планирование'
            },
            'hr': {
                name: '👥 HR Агент',
                description: 'Управление персоналом, найм, обучение и кадровое планирование'
            },
            'analytics': {
                name: '📊 Аналитический Агент',
                description: 'Анализ данных, отчеты, прогнозирование и бизнес-аналитика'
            },
            'security': {
                name: '🔒 Агент Безопасности',
                description: 'Мониторинг безопасности, аудит и защита информации'
            }
        };

        function selectAgent() {
            currentAgent = document.getElementById('agent-select').value;
            if (currentAgent) {
                const info = agentInfo[currentAgent];
                document.getElementById('agent-name').textContent = info.name;
                document.getElementById('agent-description').textContent = info.description;
                document.getElementById('agent-info').style.display = 'block';
                
                addMessage('agent', `${info.name} подключен. Чем могу помочь?`);
            } else {
                document.getElementById('agent-info').style.display = 'none';
            }
        }

        function addMessage(type, text) {
            const messagesDiv = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            
            if (type === 'agent') {
                messageDiv.innerHTML = `<strong>${agentInfo[currentAgent]?.name || 'Агент'}:</strong> ${text}`;
            } else {
                messageDiv.innerHTML = `<strong>Вы:</strong> ${text}`;
            }
            
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            
            chatHistory.push({type, text, timestamp: new Date().toISOString(), agent: currentAgent});
        }

        function sendMessage() {
            const input = document.getElementById('message-input');
            const message = input.value.trim();
            
            if (!message || !currentAgent) {
                alert('Выберите агента и введите сообщение');
                return;
            }
            
            addMessage('user', message);
            input.value = '';
            
            // Отправка сообщения агенту
            fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({agent: currentAgent, message: message})
            })
            .then(r => r.json())
            .then(data => {
                if (data.response) {
                    addMessage('agent', data.response);
                }
            })
            .catch(e => {
                addMessage('agent', 'Ошибка связи с агентом. Попробуйте позже.');
            });
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function loadChatHistory() {
            if (!currentAgent) {
                alert('Сначала выберите агента');
                return;
            }
            
            fetch(`/api/chat-history/${currentAgent}`)
                .then(r => r.json())
                .then(data => {
                    if (data.history) {
                        document.getElementById('messages').innerHTML = '';
                        data.history.forEach(msg => {
                            addMessage(msg.type, msg.text);
                        });
                    }
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def director_dashboard():
    if 'logged_in' not in session:
        return render_template_string(LOGIN_TEMPLATE)
    return render_template_string(DIRECTOR_TEMPLATE)

@app.route('/chat')
def chat_page():
    return render_template_string(CHAT_TEMPLATE)

@app.route('/api/metrics')
def api_metrics():
    # Имитация метрик системы
    return jsonify({
        "cpu": 45,
        "memory": 62,
        "disk": 78,
        "services": {
            "construction_manager": {"healthy": True},
            "accounting_agent": {"healthy": True},
            "hr_agent": {"healthy": False},
            "security_core": {"healthy": True}
        }
    })

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    agent = data.get('agent')
    message = data.get('message')
    
    # Имитация ответов агентов
    responses = {
        'construction': f"Строительный менеджер: Получил ваше сообщение '{message}'. Проверяю текущие проекты...",
        'accounting': f"Бухгалтер: Анализирую финансовые данные по запросу '{message}'...",
        'hr': f"HR агент: Обрабатываю кадровый запрос '{message}'. Проверяю базу сотрудников...",
        'analytics': f"Аналитик: Формирую отчет по запросу '{message}'. Анализирую данные...",
        'security': f"Безопасность: Проверяю безопасность запроса '{message}'. Система защищена."
    }
    
    return jsonify({"response": responses.get(agent, "Агент недоступен")})

@app.route('/api/chat-history/<agent>')
def api_chat_history(agent):
    # Имитация истории чата
    history = [
        {"type": "user", "text": "Привет! Как дела?", "timestamp": "2024-01-01T10:00:00"},
        {"type": "agent", "text": "Здравствуйте! Все отлично, готов к работе!", "timestamp": "2024-01-01T10:00:05"}
    ]
    return jsonify({"history": history})

@app.route('/api/restart-services', methods=['POST'])
def api_restart_services():
    return jsonify({"message": "Все сервисы перезапущены успешно"})

@app.route('/api/emergency-stop', methods=['POST'])
def api_emergency_stop():
    return jsonify({"message": "Аварийная остановка выполнена"})

@app.route('/api/director-login', methods=['POST'])
def api_director_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Проверка учетных данных директора
    if username == 'director' and password == 'admin2024':
        session['logged_in'] = True
        session['user_role'] = 'director'
        session['username'] = username
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Неверный логин или пароль"})

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({"message": "Выход выполнен успешно"})

@app.route('/api/backup', methods=['POST'])
def api_backup():
    return jsonify({"message": "Резервная копия создана успешно"})

@app.route('/api/staff-list')
def api_staff_list():
    # Имитация списка сотрудников
    staff = [
        {"id": 1, "name": "Иванов Иван", "position": "Прораб"},
        {"id": 2, "name": "Петров Петр", "position": "Бухгалтер"},
        {"id": 3, "name": "Сидорова Мария", "position": "HR Менеджер"},
        {"id": 4, "name": "Козлов Алексей", "position": "Аналитик"},
        {"id": 5, "name": "Новикова Ольга", "position": "Менеджер проектов"}
    ]
    return jsonify({"staff": staff})

@app.route('/api/assign-agent', methods=['POST'])
def api_assign_agent():
    data = request.get_json()
    staff_id = data.get('staff_id')
    agent_type = data.get('agent_type')
    permissions = data.get('permissions')
    
    # Сохранение назначения в базу данных
    try:
        conn = sqlite3.connect('director_system.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_id INTEGER,
                agent_type TEXT,
                permissions TEXT,
                assigned_date TEXT
            )
        ''')
        
        cursor.execute('''
            INSERT INTO agent_assignments (staff_id, agent_type, permissions, assigned_date)
            VALUES (?, ?, ?, ?)
        ''', (staff_id, agent_type, permissions, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        return jsonify({"message": f"Агент {agent_type} успешно назначен сотруднику с уровнем доступа: {permissions}"})
        
    except Exception as e:
        return jsonify({"error": f"Ошибка назначения: {str(e)}"}), 500

if __name__ == '__main__':
    print("🏢 Запуск интерфейса генерального директора...")
    print("📊 Панель управления: http://localhost:8088")
    print("💬 Чат с агентами: http://localhost:8088/chat")
    
    app.run(host='0.0.0.0', port=8088, debug=False)