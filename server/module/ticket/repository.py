from sqlalchemy.orm import Session
from models.ticket import Ticket

class TicketRepository:
    
    def create_ticket(self,db:Session, data:dict):
        ticket = Ticket(**data)
        db.add(ticket)
        db.commit()
        db.refresh(ticket)  
        return ticket
    
    
    def get_ticket(self,db:Session, ticket_id:int):
        return db.query(Ticket).filter(Ticket.id == ticket_id).first()