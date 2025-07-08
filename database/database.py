import json
from contextlib import contextmanager

import redis

import settings


async def get_redis_client():
    client = redis.from_url(
        f"redis://{settings.REDIS_HOST}:6379", decode_responses=True
    )
    try:
        yield client
    finally:
        await client.close()


@contextmanager
def redis_client():
    client = redis.Redis(host=settings.REDIS_HOST, port=6379)
    try:
        yield client
    finally:
        client.close()


def get_session(user_id):
    with redis_client() as client:
        session = client.get(user_id)
        return (
            json.loads(session)
            if session
            else {
                "state": {"action": None, "model": None, "status": None},
                "history": [],
            }
        )


def save_session(user_id, session):
    with redis_client() as client:
        client.set(user_id, json.dumps(session), ex=3600)  # expires in 1 hour
