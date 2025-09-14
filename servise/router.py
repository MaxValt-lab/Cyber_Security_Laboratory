from fastapi import APIRouter, Request
from models import Event
from processor import process_event

router = APIRouter()

@router.post("/event")
async def receive_event(event: Event, request: Request):
    result = process_event(event.dict())
    return {"status": "processed", "risk_score": result["risk_score"], "action": result["action"]}
