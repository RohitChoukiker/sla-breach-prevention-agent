from pydantic import BaseModel
from typing import Optional

class CreateTicketDTO(BaseModel):
    title: str
    description: str
    priority: str
  

class TicketResponseDTO(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    breach_probability: Optional[float]
