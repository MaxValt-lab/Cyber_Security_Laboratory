# servise/router.py

from fastapi import APIRouter, HTTPException
from .models import Event, EventResult
from .processor import process_event

router = APIRouter(tags=["events"])

@router.get("/status")
def status():
    return {"status": "ok"}

@router.post("/event", response_model=EventResult)
def receive_event(event: Event):
    try:
        result = process_event(event.model_dump())
        return EventResult(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {e}")
