from sqlalchemy import Column, ForeignKey, String, Enum, Boolean, DateTime,Float ,Integer
import datetime
from sqlalchemy.orm import relationship
from database import Base



class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255),nullable=False)
    description = Column(String(1024), nullable=False)
    priority = Column(Enum("low", "medium", "high", name="priority"), nullable=False)
    status = Column(Enum("open", "in_progress", "escalated", "closed", name="status"), default="open")
    sla_deadline = Column(DateTime, nullable=True)
    is_breached = Column(Boolean, default=False)
    breach_probability = Column(Float, nullable=True)
    confidence_score = Column(Float, nullable=True)
    ai_decision = Column(String(50), nullable=True) 
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    customer = relationship("User", foreign_keys=[customer_id])
    assigned_agent = relationship("User", foreign_keys=[assigned_agent_id])
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)