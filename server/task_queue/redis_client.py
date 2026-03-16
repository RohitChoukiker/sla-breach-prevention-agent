import os
import redis
from dotenv import load_dotenv
load_dotenv()

def get_redis_connection():

    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        print("[Redis] Connecting using REDIS_URL...")
        conn = redis.from_url(redis_url)
        print("[Redis] Connection established via URL.")
        return conn

    redis_password = os.getenv("REDIS_PASSWORD")
    print("[Redis] Connecting using host config...")
    conn = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        password=redis_password if redis_password else None,
        db=int(os.getenv("REDIS_DB", 0))
    )
    print("[Redis] Connection established via host config.")
    return conn


redis_conn = get_redis_connection()