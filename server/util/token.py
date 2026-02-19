from exceptions import AppException

def extract_bearer_token(authorization: str) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise AppException(status_code=401, detail="Missing or invalid Authorization header")
    return authorization.split(" ", 1)[1]
