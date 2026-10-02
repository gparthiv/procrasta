import time
import uuid

from config import valkey_client

SESSION_TTL = 60 * 60
SESSION_REGISTRY = "session_registry"


def create_session():
    user_id = str(uuid.uuid4())

    key = f"session:{user_id}"

    expires_at = int(time.time()) + SESSION_TTL

    valkey_client.set(
        key,
        "active",
        ex=SESSION_TTL,
    )

    valkey_client.zadd(
        SESSION_REGISTRY,
        {user_id: expires_at},
    )

    return user_id


def refresh_session(user_id: str):
    key = f"session:{user_id}"

    if not valkey_client.exists(key):
        return False

    expires_at = int(time.time()) + SESSION_TTL

    valkey_client.expire(
        key,
        SESSION_TTL,
    )

    valkey_client.zadd(
        SESSION_REGISTRY,
        {user_id: expires_at},
    )

    return True
