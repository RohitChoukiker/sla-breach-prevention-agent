from fastapi import APIRouter, Depends, Header
from util.token import extract_bearer_token
from sqlalchemy.orm import Session
from database import get_db
from DTO.user_dto import UserLoginRequest, UserSignupRequest , ChangeRoleRequest
from .service import signup_service, login_service, audit_logs_service, current_user_service, update_role_service
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security
security = HTTPBearer()


auth_router = APIRouter(prefix="/auth", tags=["auth"])




@auth_router.post("/signup")
def signup(data: UserSignupRequest, db: Session = Depends(get_db)):
    return signup_service(data, db)


@auth_router.post("/login")
async def login(data: UserLoginRequest, db: Session = Depends(get_db)):
    return await login_service(data, db)



@auth_router.get("/me")
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    return await current_user_service(token, db)




@auth_router.patch("/{user_id}/role")
async def change_role(
    user_id: str,
    data: ChangeRoleRequest,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    return await update_role_service(token, user_id, data.role, db)




@auth_router.get("/audit-logs")
async def get_audit_logs(
    authorization: str = Header(..., alias="Authorization"),
    db: Session = Depends(get_db)
):
    token = extract_bearer_token(authorization)
    return await audit_logs_service(token, db)
