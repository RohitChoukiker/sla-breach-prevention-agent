from firebase_admin import auth as firebase_auth, _auth_utils
from models.user import User
from models.enums import Role
from sqlalchemy.orm import Session
from exceptions import AppException
from DTO.admin_dto import AdminUserResponse

def create_user_service(request, admin_user, db: Session):
    
    if admin_user.role != Role.admin:
        raise AppException(403, "Only admin can create users")

    
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise AppException(400, "User with this email already exists")


    try:
        try:
            firebase_user = firebase_auth.get_user_by_email(request.email)
        except _auth_utils.UserNotFoundError:
            firebase_user = firebase_auth.create_user(
                email=request.email,
                password=request.password,
                display_name=request.name
            )
    except Exception as e:
        raise AppException(500, f"Firebase error: {str(e)}")

    
    new_user = User(
        firebase_uid=firebase_user.uid,
        email=request.email,
        password=request.password,
        name=request.name,
        role=request.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.id, "role": new_user.role}

def users_list_service(admin_user, db: Session):
    if admin_user.role != Role.admin:
        raise AppException(403, "Only admin can view users")
    users = db.query(User).filter(User.role != Role.admin).all()
    return [AdminUserResponse(
        id=u.id,
        name=u.name,
        email=u.email,
        role=u.role
    ) for u in users]
