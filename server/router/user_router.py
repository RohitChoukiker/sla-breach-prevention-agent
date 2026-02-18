from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/users")
def get_users():
    return {" test users": []}