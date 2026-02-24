from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from .service import AdminService
from DTO.admin_dto import AdminCreateUserRequest ,AssignTicketRequest, OverridePriorityRequest
from DTO.admin_dto import AdminUserResponse
from rbac.require_admin import require_admin
from rbac.role_checker import require_role
from models.enums import Role



admin_router = APIRouter(prefix="/admin", tags=["Admin"])

service = AdminService()

@admin_router.post("/create-user")
def create_user(
    data: AdminCreateUserRequest,
    admin_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return service.create_user_service(data, admin_user, db)



@admin_router.get("/all-users", response_model=list[AdminUserResponse])
def list_users(admin_user = Depends(require_admin), db: Session = Depends(get_db)):
    return service.users_list_service(admin_user, db)




# 1️⃣ View All Tickets
@admin_router.get("/tickets")
def view_all_tickets(
    user = Depends(require_role(Role.admin)),
    db: Session = Depends(get_db)
):
    return service.get_all_tickets(db)


# 2️⃣ Assign Ticket to Agent
@admin_router.patch("/tickets/{ticket_id}/assign")
def assign_ticket(
    ticket_id: str,
    data: AssignTicketRequest,
    user = Depends(require_role(Role.admin)),
    db: Session = Depends(get_db)
):
    return service.assign_ticket(db, ticket_id, data.agent_id)



@admin_router.get("/tickets/high-risk")
def high_risk_tickets(
    user = Depends(require_role(Role.admin)),
    db: Session = Depends(get_db)
):
    return service.get_high_risk_tickets(db)



@admin_router.patch("/tickets/{ticket_id}/override-priority")
def override_priority(
    ticket_id: str,
    data: OverridePriorityRequest,
    user = Depends(require_role(Role.admin)),
    db: Session = Depends(get_db)
):
    return service.override_priority(db, ticket_id, data.priority)
