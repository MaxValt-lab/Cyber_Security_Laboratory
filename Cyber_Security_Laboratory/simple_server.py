#!/usr/bin/env python3
import http.server
import socketserver
import json
import sqlite3
import os
from datetime import datetime
from urllib.parse import urlparse, parse_qs

class CyberLabHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.init_db()
        super().__init__(*args, **kwargs)
    
    def init_db(self):
        conn = sqlite3.connect('cyberlab.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                type TEXT NOT NULL,
                source TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                risk_score INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
    
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/':
            self.serve_dashboard()
        elif parsed.path == '/api/status':
            self.send_json({"status": "ok"})
        elif parsed.path == '/api/stats':
            self.send_stats()
        elif parsed.path == '/api/events':
            self.send_events()
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/event':
            self.handle_event()
        else:
            self.send_error(404)
    
    def serve_dashboard(self):
        html = '''<!DOCTYPE html>
<html><head><title>Cyber Security Lab</title>
<style>body{font-family:Arial;margin:20px;background:#f5f5f5}
.header{background:#2c3e50;color:white;padding:20px;border-radius:8px}
.stats{display:flex;gap:20px;margin:20px 0}
.stat{background:white;padding:20px;border-radius:8px;flex:1}
.events{background:white;padding:20px;border-radius:8px}
</style></head><body>
<div class="header"><h1>Cyber Security Laboratory</h1></div>
<div class="stats">
<div class="stat"><h2 id="events">0</h2><p>События</p></div>
<div class="stat"><h2 id="risk">0</h2><p>Средний риск</p></div>
</div>
<div class="events"><h2>События</h2><div id="eventsList">Загрузка...</div></div>
<script>
async function load(){
const stats=await fetch('/api/stats').then(r=>r.json());
document.getElementById('events').textContent=stats.total_events;
document.getElementById('risk').textContent=stats.avg_risk;
const events=await fetch('/api/events').then(r=>r.json());
document.getElementById('eventsList').innerHTML=events.events.map(e=>
`<div style="border-left:4px solid #3498db;padding:10px;margin:10px 0;background:#f8f9fa">
<b>${e[3]}</b> - ${e[5]} (Риск: ${e[6]})<br><small>${e[1]}</small></div>`).join('');
}
setInterval(load,10000);load();
</script></body></html>'''
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def handle_event(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            event = json.loads(post_data.decode('utf-8'))
            risk_score = self.calculate_risk(event)
            
            conn = sqlite3.connect('cyberlab.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO events (timestamp, type, source, severity, message, risk_score)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                event.get('type', 'unknown'),
                event.get('source', 'unknown'),
                event.get('severity', 'low'),
                event.get('message', ''),
                risk_score
            ))
            conn.commit()
            conn.close()
            
            self.send_json({
                "status": "processed",
                "risk_score": risk_score,
                "action": "logged"
            })
        except Exception as e:
            self.send_json({"error": str(e)}, 500)
    
    def calculate_risk(self, event):
        score = 0
        type_weights = {"login_attempt": 8, "file_access": 20, "network_scan": 35}
        source_weights = {"internal": 5, "external": 15}
        severity_weights = {"low": 5, "medium": 15, "high": 30, "critical": 50}
        
        score += type_weights.get(event.get('type'), 0)
        score += source_weights.get(event.get('source'), 0)
        score += severity_weights.get(event.get('severity'), 0)
        
        return score
    
    def send_stats(self):
        conn = sqlite3.connect('cyberlab.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM events")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(risk_score) FROM events WHERE risk_score > 0")
        avg_risk = cursor.fetchone()[0] or 0
        
        conn.close()
        
        self.send_json({
            "total_events": total,
            "avg_risk": round(avg_risk, 1)
        })
    
    def send_events(self):
        conn = sqlite3.connect('cyberlab.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events ORDER BY timestamp DESC LIMIT 10")
        events = cursor.fetchall()
        conn.close()
        
        self.send_json({"events": events})
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

if __name__ == "__main__":
    PORT = 8000
    with socketserver.TCPServer(("", PORT), CyberLabHandler) as httpd:
        print(f"Cyber Security Laboratory запущен на http://localhost:{PORT}")
        print("Веб-интерфейс: http://localhost:8000")
        print("API статус: http://localhost:8000/api/status")
        httpd.serve_forever()