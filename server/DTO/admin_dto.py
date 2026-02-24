from pydantic import BaseModel, EmailStr
from models.enums import Role
from typing import Literal


class AdminCreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Role
    
class AdminUserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: Role
    
    
    
class AssignTicketRequest(BaseModel):
    agent_id: str

class OverridePriorityRequest(BaseModel):
    priority: Literal["P1", "P2", "P3", "P4"]    