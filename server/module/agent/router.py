from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.enums import Role
from rbac.role_checker import require_role
from .service import AgentService
from DTO.agent_dto import UpdateTicketStatusRequest, AddResolutionNoteRequest

agent_router = APIRouter(prefix="/agent", tags=["Agent"])
service = AgentService()

@agent_router.get("/tickets")
def view_assigned_tickets(
    user = Depends(require_role(Role.agent)),
    db: Session = Depends(get_db)
):
    return service.get_assigned_tickets(db, user.id)


@agent_router.get("/tickets/{ticket_id}")
def view_ticket(
    ticket_id: str,
    user = Depends(require_role(Role.agent)),
    db: Session = Depends(get_db)
):
    return service.get_ticket_details(db, ticket_id, user.id)



@agent_router.patch("/tickets/{ticket_id}/status")
def update_status(
    ticket_id: str,
    request: UpdateTicketStatusRequest,
    user = Depends(require_role(Role.agent)),
    db: Session = Depends(get_db)
):
    return service.update_status(db, ticket_id, request.status, user.id)


@agent_router.patch("/tickets/{ticket_id}/resolve")
def resolve_ticket(
    ticket_id: str,
    request: AddResolutionNoteRequest,
    user = Depends(require_role(Role.agent)),
    db: Session = Depends(get_db)
):
    return service.add_resolution_note(db, ticket_id, request.note, user.id)
