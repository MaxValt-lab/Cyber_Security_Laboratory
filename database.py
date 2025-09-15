import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_path="cyberlab.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Events table
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
        
        # Incidents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                risk_score INTEGER NOT NULL,
                event_data TEXT NOT NULL,
                status TEXT DEFAULT 'open'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_event(self, event_data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO events (timestamp, type, source, severity, message, risk_score)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            event_data.get('type', 'unknown'),
            event_data.get('source', 'unknown'),
            event_data.get('severity', 'low'),
            event_data.get('message', ''),
            event_data.get('risk_score', 0)
        ))
        
        conn.commit()
        conn.close()
    
    def log_incident(self, incident_data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO incidents (timestamp, risk_score, event_data)
            VALUES (?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            incident_data.get('risk_score', 0),
            str(incident_data)
        ))
        
        conn.commit()
        conn.close()

# Global instance
db = Database()