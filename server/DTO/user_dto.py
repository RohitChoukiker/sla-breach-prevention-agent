from pydantic import BaseModel, EmailStr


class UserSignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
   
    
    
class UserLoginRequest(BaseModel):
    token: str


class ChangeRoleRequest(BaseModel):
    role: str
    