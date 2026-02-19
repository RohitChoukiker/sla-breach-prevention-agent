from sqlalchemy import Column, String, Enum, Boolean
from database import Base
from models.enums import Role
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    firebase_uid = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=True) 
    role = Column(Enum(Role), default=Role.customer)
    
