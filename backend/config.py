import os
import redis

# Read host and port from environment or fallback to defaults
VALKEY_HOST = os.getenv("VALKEY_HOST", "localhost")
VALKEY_PORT = int(os.getenv("VALKEY_PORT", 6379))

# Initialize Redis client targeting Valkey
valkey_client = redis.Redis(
    host=VALKEY_HOST, 
    port=VALKEY_PORT, 
    db=0, 
    decode_responses=True  # Converts bytes to standard string (e.g., 'value' instead of b'value')
)