from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.enums import Role
from .service import TicketService
from DTO.tickets_dto import (
    CreateTicketRequest,
    AssignTicketRequest,
    UpdateTicketStatusRequest
)
from rbac.role_checker import require_role

ticket_router = APIRouter(prefix="/tickets", tags=["Tickets"])
service = TicketService()


@ticket_router.post("/")
def create_ticket(
    data: CreateTicketRequest,
    user = Depends(require_role(Role.customer)),
    db: Session = Depends(get_db)
):
    return service.create_ticket(db, data, user)


@ticket_router.get("/my-tickets")
def my_tickets(
    user = Depends(require_role(Role.customer)),
    db: Session = Depends(get_db)
):
    return service.repo.get_by_customer(db, user.id)


@ticket_router.patch("/{ticket_id}/assign")
def assign_ticket(
    ticket_id: str,
    data: AssignTicketRequest,
    user = Depends(require_role(Role.admin)),
    db: Session = Depends(get_db)
):
    return service.assign_ticket(db, ticket_id, data.agent_id)


@ticket_router.get("/assigned")
def assigned_tickets(
    user = Depends(require_role(Role.agent)),
    db: Session = Depends(get_db)
):
    return service.repo.get_by_agent(db, user.id)


@ticket_router.patch("/{ticket_id}/status")
def update_status(
    ticket_id: str,
    data: UpdateTicketStatusRequest,
    user = Depends(require_role(Role.agent)),
    db: Session = Depends(get_db)
):
    return service.update_status(db, ticket_id, data.status, user)
