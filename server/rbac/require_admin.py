from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from module.auth.firebase import verify_token
from models.user import User
from models.enums import Role


def require_admin(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()), db: Session = Depends(get_db)):
    token = credentials.credentials
    decoded = verify_token(token)
    if not decoded:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    firebase_uid = decoded["uid"]
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if not user or user.role != Role.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user
