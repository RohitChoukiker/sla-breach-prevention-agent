from pydantic import BaseModel
from typing import Literal, Optional

class UpdateTicketStatusRequest(BaseModel):
    status: Literal["in_progress", "resolved", "closed"]

class AddResolutionNoteRequest(BaseModel):
    note: str
