import http.server
import json
import sqlite3
from datetime import datetime
from urllib.parse import urlparse

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''<!DOCTYPE html>
<html><head><title>Cyber Security Lab</title></head>
<body><h1>Cyber Security Laboratory</h1>
<p>Status: Running</p>
<p>API: <a href="/api/status">/api/status</a></p>
</body></html>''')
        elif self.path == '/api/status':
            self.send_json({"status": "ok", "service": "cyber-lab"})
        else:
            self.send_error(404)
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

if __name__ == "__main__":
    PORT = 8080
    with http.server.HTTPServer(("", PORT), Handler) as httpd:
        print(f"Server running on http://localhost:{PORT}")
        httpd.serve_forever()