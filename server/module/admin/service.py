from firebase_admin import auth as firebase_auth, _auth_utils
from models.user import User
from models.ticket import Ticket
from models.enums import Role
from sqlalchemy.orm import Session
from exceptions import AppException
from DTO.admin_dto import AdminUserResponse
from module.auth.service import update_role_service, audit_logs_service


class AdminService:

    def create_user_service(self, admin_user, request, db: Session):

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

        return {
            "message": "User created successfully",
            "user_id": new_user.id,
            "role": new_user.role
        }

    def users_list_service(self, admin_user, db: Session):

        if admin_user.role != Role.admin:
            raise AppException(403, "Only admin can view users")

        users = db.query(User).filter(User.role != Role.admin).all()

        return [
            AdminUserResponse(
                id=u.id,
                name=u.name,
                email=u.email,
                role=u.role
            )
            for u in users
        ]

    def get_all_tickets(self, db: Session):
        return db.query(Ticket).all()

    def get_ticket_details(self, db: Session, ticket_id: str):
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

        if not ticket:
            raise AppException(404, "Ticket not found")

        return ticket

    def assign_ticket(self, db: Session, ticket_id: str, agent_id: str):

        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise AppException(404, "Ticket not found")

        agent = db.query(User).filter(User.id == agent_id).first()
        if not agent or agent.role != Role.agent:
            raise AppException(400, "Invalid agent")

        ticket.assigned_agent_id = agent_id
        ticket.status = "in_progress"

        db.commit()
        db.refresh(ticket)

        return ticket

    def get_high_risk_tickets(self, db: Session):

        return db.query(Ticket).filter(
            Ticket.breach_probability >= 0.8
        ).all()

    def override_priority(self, db: Session, ticket_id: str, priority: str):

        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

        if not ticket:
            raise AppException(404, "Ticket not found")

        ticket.priority_final = priority

        db.commit()
        db.refresh(ticket)

        return ticket

    async def change_role_service(self, token: str, user_id: str, role: str, db: Session):
        return await update_role_service(token, user_id, role, db)

    async def audit_logs_service(self, token: str, db: Session):
        return await audit_logs_service(token, db)