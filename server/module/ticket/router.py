from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from database import get_db
from DTO.tickets_dto import CreateTicketDTO
from .service import TicketService



ticket_router = APIRouter(prefix="/tickets", tags=["Tickets"])
ticket_service = TicketService()




@ticket_router.post("/create-ticket")
async def create_tickets(data: CreateTicketDTO, db: Session = Depends(get_db)):
    return ticket_service.create_ticket_service(db, data.dict())


@ticket_router.get("/{ticket_id}")
async def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    return ticket_service.get_ticket_service(db, ticket_id)