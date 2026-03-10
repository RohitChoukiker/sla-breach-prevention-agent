import os
import redis


def get_redis_connection():
    redis_url = os.getenv("REDIS_URL")

    # If REDIS_URL exists use it
    if redis_url:
        print("[Redis] Connecting using REDIS_URL...")
        conn = redis.from_url(
            redis_url,
            decode_responses=True
        )
        print("[Redis] Connection established via URL.")
        return conn

    # Otherwise use host config
    redis_password = os.getenv("REDIS_PASSWORD")
    print("[Redis] Connecting using host config...")
    conn = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        password=redis_password if redis_password else None,
        db=int(os.getenv("REDIS_DB", 0)),
        decode_responses=True
    )
    print("[Redis] Connection established via host config.")
    return conn


redis_conn = get_redis_connection()


def check_redis_health():
    try:
        redis_conn.ping()
        return True
    except redis.exceptions.ConnectionError:
        return False