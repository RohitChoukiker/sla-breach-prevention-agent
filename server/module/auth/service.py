
from firebase_admin import auth as firebase_auth
from exceptions import AppException
from sqlalchemy.orm import Session
from models.user import User
from .firebase import verify_token
from models.enums import Role
from util.audit_log import log_audit_event, get_audit_logs

async def audit_logs_service(token: str, db: Session):
    decoded = verify_token(token)
    if not decoded:
        raise AppException(401, "Invalid token")
    firebase_uid = decoded["uid"]
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if not user or user.role != Role.admin:
        raise AppException(403, "Only admin can view audit logs")
    return {"logs": get_audit_logs()}


async def signup_service(data, db: Session):
    role = Role.customer

    try:
        existing_user = db.query(User).filter(User.email == data.email).first()
        if existing_user:
            raise AppException(400, "Email already registered")

      
        firebase_user = firebase_auth.create_user(
            email=data.email,
            password=data.password,
            display_name=data.name
        )

        new_user = User(
            firebase_uid=firebase_user.uid,
            email=data.email,
            name=data.name,
            role=role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        verification_link = firebase_auth.generate_email_verification_link(
            data.email
        )

        log_audit_event("signup", new_user.id, f"User signed up: {new_user.email}")

        return {
            "message": "User created successfully",
            "user_id": new_user.id,
            "verification_link": verification_link,
        }

    except AppException:
        raise

    except Exception:
        db.rollback()
        raise AppException(500, "Internal server error")



async def login_service(data, db: Session):

    decoded = verify_token(data.token)

    if not decoded:
        raise AppException(401, "Invalid token")

    if not decoded.get("email_verified"):
        raise AppException(403, "Email not verified")

    firebase_uid = decoded["uid"]

    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()

    if not user:
        raise AppException(404, "User not found")

    

    return {
        "message": "Login successful",
        "name": user.name,
        "email": user.email,
        "role": user.role,
    }



async def current_user_service(token: str, db: Session):

    decoded = verify_token(token)

    if not decoded:
        raise AppException(401, "Invalid token")

    firebase_uid = decoded["uid"]

    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()

    if not user:
        raise AppException(404, "User not found")

    return {
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "firebase_uid": user.firebase_uid,
    }


import asyncio
async def update_role_service(token: str, user_id: str, new_role: str, db: Session):
  
    decoded = verify_token(token)
    if not decoded:
        raise AppException(401, "Invalid token")
    firebase_uid = decoded["uid"]
    requester = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if not requester or requester.role != Role.admin:
        raise AppException(403, "Only admin can change roles")
  
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise AppException(404, "User not found")
    if new_role not in Role.__members__:
        raise AppException(400, "Invalid role")
    user.role = Role[new_role]
    db.commit()
    db.refresh(user)
    log_audit_event("change_role", user.id, f"Role changed to {user.role} by admin {requester.email}")
    return {"message": f"Role changed to {user.role}", "user_id": user.id, "role": user.role}