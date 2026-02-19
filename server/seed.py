
import os
from sqlalchemy.orm import Session
from models.enums import Role
from models.user import User
from firebase_admin import auth as firebase_auth, _auth_utils



def seed_admin(db: Session):
    existing_admin = db.query(User).filter(User.role == Role.admin).first()
    if existing_admin:
        print("Admin user already exists. Skipping seeding.")
        return

    admin_email = os.environ.get("ADMIN_EMAIL")
    admin_pass = os.environ.get("ADMIN_PASSWORD")
    admin_firebase_uid = os.environ.get("ADMIN_FIREBASE_UID")
    if not admin_firebase_uid:
        raise ValueError("ADMIN_FIREBASE_UID environment variable not set. Please set it to the admin's Firebase UID.")

    # Create admin in Firebase if not exists
    try:
        firebase_user = firebase_auth.get_user_by_email(admin_email)
        print(f"Admin already exists: {firebase_user.uid}")
    except _auth_utils.UserNotFoundError:
        firebase_user = firebase_auth.create_user(
            uid=admin_firebase_uid,
            email=admin_email,
            password=admin_pass,
            display_name="Admin"
        )
        print(f"Admin user created in Firebase: {firebase_user.uid}")

    
    admin_user = User(
        firebase_uid=firebase_user.uid,
        email=admin_email,
        password=admin_pass,
        role=Role.admin
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    print("Admin user seeded successfully.")