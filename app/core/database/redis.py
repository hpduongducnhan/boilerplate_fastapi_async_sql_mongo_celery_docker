# -*- coding: utf-8 -*-
from typing import Union, Any
import aioredis
import aioredis.sentinel
from aioredis.client import PubSub, Redis
from app.config import settings


CLIENT_TYPE_PUB = 'type-pub'
CLIENT_TYPE_SUB = 'type-sub'


# normal connect redis
redis_client = aioredis.from_url(
    f"redis://:{settings.APP_REDIS_PASSWORD}@{settings.APP_REDIS_HOST}:{settings.APP_REDIS_PORT}/{settings.APP_REDIS_DB}",
    decode_responses=True
)


# sentinel for production
# sentinel = aioredis.sentinel.Sentinel([
#     "redis://localhost:26379",
#     "redis://sentinel2:26379"
# ])
# redis_client = sentinel.master_for("mymaster")


async def get_subscribe_channel(client: Redis, channel: str) -> PubSub:
    pubsub = client.pubsub()
    await pubsub.subscribe(channel)
    return pubsub
