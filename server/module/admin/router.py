from fastapi import APIRouter, Depends
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from .service import AdminService
from DTO.admin_dto import (
    AdminCreateUserRequest,
    AssignTicketRequest,
    OverridePriorityRequest,
    AdminUserResponse
)
from DTO.user_dto import ChangeRoleRequest
from rbac.require_admin import require_admin

admin_router = APIRouter(prefix="/admin", tags=["Admin"])
security = HTTPBearer()

service = AdminService()


@admin_router.post("/create-user")
def create_user(
    data: AdminCreateUserRequest,
    admin_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return service.create_user_service(admin_user, data, db)


@admin_router.get("/all-users", response_model=list[AdminUserResponse])
def list_users(
    admin_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return service.users_list_service(admin_user, db)


@admin_router.get("/tickets")
def view_all_tickets(
    admin_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return service.get_all_tickets(db)


@admin_router.patch("/tickets/{ticket_id}/assign")
def assign_ticket(
    ticket_id: str,
    data: AssignTicketRequest,
    admin_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return service.assign_ticket(db, ticket_id, data.agent_id)


@admin_router.get("/tickets/high-risk")
def high_risk_tickets(
    admin_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return service.get_high_risk_tickets(db)


@admin_router.get("/tickets/{ticket_id}")
def view_ticket_details(
    ticket_id: str,
    admin_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return service.get_ticket_details(db, ticket_id)


@admin_router.patch("/tickets/{ticket_id}/override-priority")
def override_priority(
    ticket_id: str,
    data: OverridePriorityRequest,
    admin_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return service.override_priority(db, ticket_id, data.priority)


@admin_router.patch("/{user_id}/role")
async def change_role(
    user_id: str,
    data: ChangeRoleRequest,
    crednticals: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    token = crednticals.credentials
    return await service.change_role_service(token, user_id, data.role, db)


@admin_router.get("/audit-logs")
async def get_audit_logs(
    crednticals: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    token = crednticals.credentials
    return await service.audit_logs_service(token, db)