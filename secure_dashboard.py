"""
Защищенная панель управления с усиленной безопасностью
"""
from flask import Flask, request, jsonify, session, render_template_string
import jwt
from datetime import datetime, timedelta
from security_core import security_core
from data_protection import data_protection
from failover_manager import failover_manager
import logging

app = Flask(__name__)
app.secret_key = security_core.master_key

# HTML шаблон
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Management Dashboard</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .status-ok { color: green; } .status-error { color: red; }
        .btn { padding: 10px 20px; margin: 5px; border: none; border-radius: 4px; cursor: pointer; }
        .btn-primary { background: #007bff; color: white; }
        .btn-danger { background: #dc3545; color: white; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .log-entry { font-family: monospace; font-size: 12px; padding: 5px; border-left: 3px solid #007bff; margin: 5px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 Secure Management Dashboard</h1>
        
        <div class="grid">
            <div class="card">
                <h3>System Status</h3>
                <div id="system-status">Loading...</div>
                <button class="btn btn-primary" onclick="refreshStatus()">Refresh</button>
            </div>
            
            <div class="card">
                <h3>Security Metrics</h3>
                <div id="security-metrics">Loading...</div>
            </div>
            
            <div class="card">
                <h3>Backup Status</h3>
                <div id="backup-status">Loading...</div>
                <button class="btn btn-primary" onclick="createBackup()">Create Backup</button>
            </div>
            
            <div class="card">
                <h3>Access Control</h3>
                <div id="access-control">Loading...</div>
            </div>
        </div>
        
        <div class="card">
            <h3>Recent Activity</h3>
            <div id="activity-log">Loading...</div>
        </div>
        
        <div class="card">
            <h3>Emergency Controls</h3>
            <button class="btn btn-danger" onclick="emergencyShutdown()">Emergency Shutdown</button>
            <button class="btn btn-primary" onclick="restartServices()">Restart All Services</button>
        </div>
    </div>

    <script>
        function refreshStatus() {
            fetch('/api/status')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('system-status').innerHTML = formatStatus(data);
                });
        }
        
        function formatStatus(data) {
            let html = '<ul>';
            for (let service in data.services) {
                let status = data.services[service];
                let statusClass = status.healthy ? 'status-ok' : 'status-error';
                html += `<li class="${statusClass}">${service}: ${status.healthy ? 'OK' : 'DOWN'} (Port: ${status.port})</li>`;
            }
            html += '</ul>';
            html += `<p>CPU: ${data.system.cpu_percent}% | Memory: ${data.system.memory_percent}%</p>`;
            return html;
        }
        
        function createBackup() {
            fetch('/api/backup', {method: 'POST'})
                .then(r => r.json())
                .then(data => alert(data.message));
        }
        
        function emergencyShutdown() {
            if (confirm('Are you sure you want to perform emergency shutdown?')) {
                fetch('/api/emergency-shutdown', {method: 'POST'})
                    .then(r => r.json())
                    .then(data => alert(data.message));
            }
        }
        
        function restartServices() {
            fetch('/api/restart-services', {method: 'POST'})
                .then(r => r.json())
                .then(data => alert(data.message));
        }
        
        // Auto-refresh every 30 seconds
        setInterval(refreshStatus, 30000);
        
        // Initial load
        refreshStatus();
    </script>
</body>
</html>
"""

@app.before_request
def security_check():
    """Проверка безопасности перед каждым запросом"""
    # Проверка IP (можно добавить whitelist)
    client_ip = request.remote_addr
    
    # Проверка сессии для защищенных эндпоинтов
    if request.endpoint and request.endpoint.startswith('api_'):
        token = request.headers.get('Authorization') or session.get('token')
        if not token:
            return jsonify({"error": "Authentication required"}), 401
        
        session_data = security_core.validate_session(token)
        if not session_data:
            return jsonify({"error": "Invalid session"}), 401
        
        request.user_data = session_data

@app.route('/')
def dashboard():
    """Главная страница панели управления"""
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/api/login', methods=['POST'])
def login():
    """Аутентификация"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Проверка учетных данных (упрощенная)
    if username == "admin" and password == "secure2024":
        user_data = {"username": username, "role": "admin"}
        token = security_core.create_session(user_data)
        session['token'] = token
        
        security_core.audit_log("login", username, {"ip": request.remote_addr})
        
        return jsonify({"token": token, "message": "Login successful"})
    else:
        data_protection.record_failed_attempt(username)
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/status')
def api_status():
    """Статус системы"""
    status = failover_manager.get_system_status()
    return jsonify(status)

@app.route('/api/backup', methods=['POST'])
def api_backup():
    """Создание резервной копии"""
    try:
        db_paths = ["director_system.db", "general_system.db", "cyberlab.db"]
        for db_path in db_paths:
            security_core.backup_database(db_path)
        
        security_core.audit_log("manual_backup", request.user_data['user']['username'], {})
        return jsonify({"message": "Backup created successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/emergency-shutdown', methods=['POST'])
def api_emergency_shutdown():
    """Аварийное отключение"""
    try:
        failover_manager.emergency_shutdown()
        security_core.audit_log("emergency_shutdown", request.user_data['user']['username'], {})
        return jsonify({"message": "Emergency shutdown initiated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/restart-services', methods=['POST'])
def api_restart_services():
    """Перезапуск сервисов"""
    try:
        for service_name in failover_manager.services.keys():
            failover_manager.restart_service(service_name)
        
        security_core.audit_log("services_restart", request.user_data['user']['username'], {})
        return jsonify({"message": "Services restart initiated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/security-metrics')
def api_security_metrics():
    """Метрики безопасности"""
    metrics = {
        "access_report": data_protection.get_access_report(),
        "backup_count": len([f for f in os.listdir("backups") if f.endswith('.enc')]) if os.path.exists("backups") else 0,
        "system_uptime": time.time() - app.start_time if hasattr(app, 'start_time') else 0
    }
    return jsonify(metrics)

if __name__ == '__main__':
    app.start_time = time.time()
    
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)
    
    print("🔒 Starting Secure Management Dashboard...")
    print("📊 Dashboard: http://localhost:8085")
    print("🔐 Default credentials: admin/secure2024")
    
    app.run(host='0.0.0.0', port=8085, debug=False)