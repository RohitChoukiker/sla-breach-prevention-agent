from models.ticket import Ticket

class TicketRepository:

    def create(self, db, ticket: Ticket):
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket

    def get_by_id(self, db, ticket_id: str):
        return db.query(Ticket).filter(
            Ticket.id == ticket_id
        ).first()

    def get_by_customer(self, db, customer_id: str):
        return db.query(Ticket).filter(
            Ticket.customer_id == customer_id
        ).all()

    def get_by_agent(self, db, agent_id: str):
        return db.query(Ticket).filter(
            Ticket.assigned_agent_id == agent_id
        ).all()
