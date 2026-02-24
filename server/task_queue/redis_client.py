import os
import redis

def get_redis_connection():

    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        return redis.from_url(
            redis_url,
            decode_responses=True
        )
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        password=os.getenv("REDIS_PASSWORD", None),
        db=int(os.getenv("REDIS_DB", 0)),
        decode_responses=True
    )

redis_conn = get_redis_connection()

def check_redis_health():
    try:
        redis_conn.ping()
        return True
    except redis.exceptions.ConnectionError:
        return False
