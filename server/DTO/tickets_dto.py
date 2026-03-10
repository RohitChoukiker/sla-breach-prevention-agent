from pydantic import BaseModel
from typing import Optional, Literal

class CreateTicketRequest(BaseModel):
    title: str
    description: str
    priority: Literal["low", "medium", "high"]
  

class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    breach_probability: Optional[float]


class AssignTicketRequest(BaseModel):
    agent_id: str
    
    
class UpdateTicketStatusRequest(BaseModel):
    status: Literal["open", "in_progress", "escalated", "resolved", "closed"]