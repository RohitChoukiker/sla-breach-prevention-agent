from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from DTO.user_dto import UserLoginRequest, UserSignupRequest
from .service import signup_service, login_service, current_user_service
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security
security = HTTPBearer()


auth_router = APIRouter(prefix="/auth", tags=["auth"])




@auth_router.post("/signup")
def signup(
    data: UserSignupRequest,
    db: Session = Depends(get_db)
):
    return signup_service(data, db)


@auth_router.post("/login")
async def login(data: UserLoginRequest, db: Session = Depends(get_db)):
    return await login_service(data, db)



@auth_router.get("/me")
async def get_current_user(
    crednticals: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    token = crednticals.credentials
    return await current_user_service(token, db)
