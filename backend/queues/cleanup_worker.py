import time

from queues.session_cleanup import cleanup_expired_sessions


while True:

    try:
        cleanup_expired_sessions()

    except Exception as e:

        print(
            f"Cleanup error: {e}"
        )

    time.sleep(60)