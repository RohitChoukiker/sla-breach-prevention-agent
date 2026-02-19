# module/admin/router.py


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from .service import create_user_service, users_list_service
from DTO.admin_dto import AdminCreateUserRequest
from DTO.admin_dto import AdminUserResponse
from rbac.require_admin import require_admin



admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.post("/create-user")
def create_user(
    request: AdminCreateUserRequest,
    admin_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return create_user_service(request, admin_user, db)



@admin_router.get("/all-users", response_model=list[AdminUserResponse])
def list_users(admin_user = Depends(require_admin), db: Session = Depends(get_db)):
    return users_list_service(admin_user, db)
