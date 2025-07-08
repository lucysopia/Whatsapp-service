from huey import PriorityRedisHuey, SqliteHuey
from redis import ConnectionPool

import settings

if settings.ENVIRONMENT in ["staging", "prod"]:
    huey = PriorityRedisHuey(
        name="ai-bot-huey",
        results=False,
        immediate=False,
        utc=True,
        blocking=True,
        connection_pool=ConnectionPool(
            host=settings.REDIS_HOST, port=6379, max_connections=20
        ),
    )
else:
    huey = SqliteHuey(filename="huey.db", immediate=False)