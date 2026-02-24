from fastapi import Depends
from module.auth.router import get_current_user
from exceptions import AppException

def require_role(required_role):
    def role_checker(user = Depends(get_current_user)):
        if user["role"] != required_role:
            raise AppException(403, "Access denied")
        return user
    return role_checker
