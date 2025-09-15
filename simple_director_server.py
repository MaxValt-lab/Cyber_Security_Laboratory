"""
Простой веб-сервер директора без внешних зависимостей
"""
import http.server
import socketserver
import json
import urllib.parse
from datetime import datetime

class DirectorHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/login':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(LOGIN_PAGE.encode('utf-8'))
        elif self.path == '/dashboard':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(DASHBOARD_PAGE.encode('utf-8'))
        elif self.path == '/chat':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(CHAT_PAGE.encode('utf-8'))
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            if data.get('username') == 'director' and data.get('password') == 'admin2024':
                response = {"success": True, "redirect": "/dashboard"}
            else:
                response = {"success": False, "error": "Неверный логин или пароль"}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

LOGIN_PAGE = """
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
            
            fetch('/api/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, password})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/dashboard';
                } else {
                    document.getElementById('error').textContent = data.error;
                }
            });
        }
    </script>
</body>
</html>
"""

DASHBOARD_PAGE = """
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
        .metric-value { font-size: 2em; font-weight: bold; color: #ffd700; }
        .chat-btn { 
            position: fixed; bottom: 30px; right: 30px;
            width: 60px; height: 60px; border-radius: 50%;
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            border: none; cursor: pointer; font-size: 24px;
            box-shadow: 0 5px 20px rgba(255,215,0,0.4);
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
                <p>CPU: <span class="metric-value">45</span>%</p>
                <p>Память: <span class="metric-value">62</span>%</p>
                <p>Диск: <span class="metric-value">78</span>%</p>
                <button class="btn">Обновить</button>
            </div>

            <div class="card">
                <h3>🔧 Управление Сервисами</h3>
                <p>✅ Строительный менеджер</p>
                <p>✅ Бухгалтерский агент</p>
                <p>❌ HR агент</p>
                <p>✅ Агент безопасности</p>
                <button class="btn">Перезапустить Все</button>
                <button class="btn btn-danger">Аварийная Остановка</button>
            </div>

            <div class="card">
                <h3>💼 Управление Проектами</h3>
                <button class="btn">Менеджер Проектов</button>
                <button class="btn">Финансы</button>
                <button class="btn">Кадры</button>
            </div>

            <div class="card">
                <h3>📈 Аналитика</h3>
                <div class="metric-value">12</div>
                <p>Активных проектов</p>
                <div class="metric-value">₽2.5М</div>
                <p>Общая выручка</p>
                <button class="btn">Создать Отчет</button>
            </div>

            <div class="card">
                <h3>👥 Команда</h3>
                <p>Онлайн сотрудников: <span class="metric-value">8</span></p>
                <p>Активных задач: <span class="metric-value">24</span></p>
                <button class="btn">Панель Команды</button>
                <button class="btn">Назначить Агента</button>
            </div>

            <div class="card">
                <h3>🔒 Безопасность</h3>
                <p>✅ Система защищена</p>
                <p>Последний бэкап: сегодня 14:30</p>
                <button class="btn">Создать Бэкап</button>
                <button class="btn">Журнал Аудита</button>
            </div>
        </div>
    </div>

    <button class="chat-btn" onclick="openChat()" title="Открыть чат с агентами">💬</button>

    <script>
        function logout() {
            if (confirm('Выйти из системы?')) {
                window.location.href = '/';
            }
        }
        
        function openChat() {
            window.open('/chat', 'chat', 'width=800,height=600');
        }
    </script>
</body>
</html>
"""

CHAT_PAGE = """
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
        .send-btn { 
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            color: #1e3c72; border: none; padding: 12px 20px;
            border-radius: 8px; cursor: pointer; font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="chat-header">
        <h2>💬 Чат с Агентами</h2>
        <select class="agent-selector" id="agent-select">
            <option value="">Выберите агента</option>
            <option value="construction">🏗️ Строительный Менеджер</option>
            <option value="accounting">💰 Бухгалтерский Агент</option>
            <option value="hr">👥 HR Агент</option>
            <option value="analytics">📊 Аналитический Агент</option>
            <option value="security">🔒 Агент Безопасности</option>
        </select>
    </div>

    <div class="chat-container">
        <div class="messages" id="messages">
            <div class="message agent">
                <strong>Система:</strong> Добро пожаловать! Выберите агента для начала общения.
            </div>
        </div>

        <div class="message-input">
            <input type="text" id="message-input" placeholder="Введите сообщение...">
            <button class="send-btn" onclick="sendMessage()">Отправить</button>
        </div>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('message-input');
            const message = input.value.trim();
            const agent = document.getElementById('agent-select').value;
            
            if (!message || !agent) {
                alert('Выберите агента и введите сообщение');
                return;
            }
            
            addMessage('user', message);
            input.value = '';
            
            // Имитация ответа агента
            setTimeout(() => {
                addMessage('agent', `${agent} агент: Получил ваше сообщение "${message}". Обрабатываю запрос...`);
            }, 1000);
        }
        
        function addMessage(type, text) {
            const messagesDiv = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            messageDiv.innerHTML = `<strong>${type === 'user' ? 'Вы' : 'Агент'}:</strong> ${text}`;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    PORT = 8089
    
    print("Director Server Starting...")
    print(f"Login page: http://localhost:{PORT}")
    print(f"Credentials: director / admin2024")
    print("Press Ctrl+C to stop")
    
    with socketserver.TCPServer(("", PORT), DirectorHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")
            httpd.shutdown()