from models.ticket import Ticket
from exceptions import AppException
from .repository import TicketRepository
from task_queue.producer import publish_ticket_event


class TicketService:

    def __init__(self):
        self.repo = TicketRepository()

    def create_ticket(self, db, request, user):

        ticket = Ticket(
            title=request.title,
            description=request.description,
            urgency_requested=request.urgency,
            customer_id=user.id,
            tenant_id=user.tenant_id,
            processing_status="pending"
        )

        ticket = self.repo.create(db, ticket)

        # 🔥 Trigger AI async processing
        publish_ticket_event(ticket.id)

        return ticket

    def assign_ticket(self, db, ticket_id, agent_id):

        ticket = self.repo.get_by_id(db, ticket_id)

        if not ticket:
            raise AppException(404, "Ticket not found")

        ticket.assigned_agent_id = agent_id
        ticket.status = "in_progress"

        db.commit()
        db.refresh(ticket)
        return ticket

    def update_status(self, db, ticket_id, status, user):

        ticket = self.repo.get_by_id(db, ticket_id)

        if not ticket:
            raise AppException(404, "Ticket not found")

        if ticket.assigned_agent_id != user.id:
            raise AppException(403, "Not assigned to you")

        ticket.status = status

        db.commit()
        db.refresh(ticket)
        return ticket
