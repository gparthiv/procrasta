import time

from config import valkey_client
from rag.cleanup import delete_user_data

SESSION_REGISTRY = "session_registry"


def cleanup_expired_sessions():

    now = int(time.time())

    expired_users = valkey_client.zrangebyscore(
        SESSION_REGISTRY,
        "-inf",
        now,
    )

    for user_id in expired_users:

        session_key = f"session:{user_id}"

        if valkey_client.exists(session_key):
            continue

        delete_user_data(user_id)

        valkey_client.zrem(
            SESSION_REGISTRY,
            user_id,
        )

        print(f"Cleaned up expired session: {user_id}")
