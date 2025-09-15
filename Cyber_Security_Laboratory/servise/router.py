# servise/router.py

from fastapi import APIRouter, HTTPException
from .models import Event, EventResult
from .processor import process_event
from database import db
import sqlite3

router = APIRouter(tags=["events"])

@router.get("/status")
def status():
    return {"status": "ok"}

@router.get("/health")
def health():
    return {"status": "healthy", "service": "cyber-security-laboratory"}

@router.post("/event", response_model=EventResult)
def receive_event(event: Event):
    try:
        result = process_event(event.model_dump())
        return EventResult(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {e}")

@router.get("/events")
def get_events(limit: int = 100):
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events ORDER BY timestamp DESC LIMIT ?", (limit,))
    events = cursor.fetchall()
    conn.close()
    return {"events": events}

@router.get("/incidents")
def get_incidents(limit: int = 50):
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents ORDER BY timestamp DESC LIMIT ?", (limit,))
    incidents = cursor.fetchall()
    conn.close()
    return {"incidents": incidents}

@router.get("/stats")
def get_stats():
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM events")
    total_events = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM incidents")
    total_incidents = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(risk_score) FROM events WHERE risk_score > 0")
    avg_risk = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return {
        "total_events": total_events,
        "total_incidents": total_incidents,
        "average_risk_score": round(avg_risk, 2)
    }
