from pydantic import BaseModel, EmailStr
from models.enums import Role


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
    