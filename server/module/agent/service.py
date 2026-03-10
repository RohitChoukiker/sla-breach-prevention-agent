from models.ticket import Ticket
from exceptions import AppException

class AgentService:

    @staticmethod
    def _normalize_status(status: str) -> str:
        normalized = status.strip().lower()
        if normalized == "resolved":
            return "closed"
        if normalized in {"in_progress", "closed"}:
            return normalized
        raise AppException(400, "Invalid status")

    def get_assigned_tickets(self, db, agent_id):
        return db.query(Ticket).filter(
            Ticket.assigned_agent_id == agent_id
        ).all()

    def get_ticket_details(self, db, ticket_id, agent_id):
        ticket = db.query(Ticket).filter(
            Ticket.id == ticket_id
        ).first()

        if not ticket:
            raise AppException(404, "Ticket not found")

        if ticket.assigned_agent_id != agent_id:
            raise AppException(403, "Not your ticket")

        return ticket

    def update_status(self, db, ticket_id, status, agent_id):
        ticket = self.get_ticket_details(db, ticket_id, agent_id)

        ticket.status = self._normalize_status(status)
        db.commit()
        db.refresh(ticket)

        return ticket

    def add_resolution_note(self, db, ticket_id, note, agent_id):
        ticket = self.get_ticket_details(db, ticket_id, agent_id)

        ticket.resolution_note = note
        ticket.status = "closed"

        db.commit()
        db.refresh(ticket)

        return ticket
