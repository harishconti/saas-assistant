import os
from agno.db.redis import RedisDb

def get_redis_storage(session_id: str = "default_session") -> RedisDb:
    """
    Returns an Agno Redis storage instance for short-term conversational 
    memory (e.g., keeping track of the last few messages in a thread).
    Requires a running Redis instance (provided by docker-compose).
    """
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    return RedisDb(
        db_url=redis_url,
        session_table="agent_sessions"
    )
