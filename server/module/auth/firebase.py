import os
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent 

cred_file = os.getenv("FIREBASE_CREDENTIALS_FILE")

if not cred_file:
    raise ValueError("FIREBASE_CREDENTIALS_FILE not set in environment")

cred_path = BASE_DIR / cred_file

if not cred_path.exists():
    raise FileNotFoundError(f"Firebase credentials file not found at {cred_path}")

certificate = credentials.Certificate(str(cred_path))

if not firebase_admin._apps:
    firebase_admin.initialize_app(certificate)


def verify_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Error verifying token: {e}")
        return None
