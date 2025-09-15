# test/test_service.py

import pytest
from fastapi.testclient import TestClient
from servise.main import app

client = TestClient(app)

def test_status():
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_event_valid():
    payload = {
        "type": "system_event",
        "source": "internal",
        "severity": "high",
        "message": "CI/CD: запуск тестов"
    }
    response = client.post("/api/event", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert "action" in data
    assert data["status"] == "processed"

def test_event_invalid():
    payload = {
        "type": "system_event",
        "source": "internal",
        # severity отсутствует
        "message": "Неполные данные"
    }
    response = client.post("/api/event", json=payload)
    assert response.status_code == 422  # Unprocessable Entity
