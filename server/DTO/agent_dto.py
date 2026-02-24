from pydantic import BaseModel
from typing import Literal, Optional

class UpdateTicketStatusRequest(BaseModel):
    status: Literal["in_progress", "resolved"]

class AddResolutionNoteRequest(BaseModel):
    note: str
