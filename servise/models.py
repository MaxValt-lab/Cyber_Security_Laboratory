# servise/models.py

from pydantic import BaseModel, Field

class Event(BaseModel):
    type: str = Field(..., description="Тип события, напр. system_event")
    source: str = Field(..., description="Источник события, напр. internal/external")
    severity: str = Field(..., description="Уровень важности: low/medium/high/critical")
    message: str = Field(..., description="Описание события")

class EventResult(BaseModel):
    status: str
    risk_score: int
    action: str
