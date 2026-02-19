from .repository import TicketRepository



class TicketService:
    def __init__(self):
        self.repository = TicketRepository()
    
    def create_ticket_service(self, db, ticket_data):
        return self.repository.create_ticket(db, ticket_data)
    
    def get_ticket_service(self, db, ticket_id):
        return self.repository.get_ticket(db, ticket_id)    