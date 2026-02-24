from typing import TypedDict, List

class TicketState(TypedDict):
    ticket_id: str
    tenant_id: str
    description: str
    urgency: str

    embedding: List[float]
    similar_count: int

    breach_probability: float
    confidence_score: float
    priority: str

    escalation_required: bool
    loop_count: int
