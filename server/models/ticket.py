from sqlalchemy import Column, String, Enum, Boolean, Float
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    title = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=False)

    urgency_requested = Column(
        Enum("low", "medium", "high", "critical", name="urgency"),
        nullable=False
    )

    priority_final = Column(String, nullable=True)

    breach_probability = Column(Float, nullable=True)
    confidence_score = Column(Float, nullable=True)

    status = Column(
        Enum("open", "in_progress", "escalated", "closed", name="status"),
        default="open"
    )

    processing_status = Column(
        Enum("pending", "processing", "completed", name="processing_status"),
        default="pending"
    )

    tenant_id = Column(String, index=True)

    customer_id = Column(String, nullable=False)
    assigned_agent_id = Column(String, nullable=True)
