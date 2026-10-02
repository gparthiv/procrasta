from redis import Redis
from rq import Queue

from config import VALKEY_HOST, VALKEY_PORT

redis_connection = Redis(
    host=VALKEY_HOST,
    port=VALKEY_PORT,
    db=0,
)

chat_queue = Queue(
    name="chat",
    connection=redis_connection,
)

ingestion_queue = Queue(
    name="ingestion",
    connection=redis_connection,
)