import os
from dotenv import load_dotenv
from redis_om import get_redis_connection

load_dotenv()

redis = get_redis_connection(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD") or None,
    decode_responses=True
)