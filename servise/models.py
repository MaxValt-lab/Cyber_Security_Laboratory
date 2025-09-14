from pydantic import BaseModel

class Event(BaseModel):
    type: str
    source: str
    severity: str
    message: str
