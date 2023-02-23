import databases
import aioredis
from core.config import settings

database = databases.Database(settings.DATABASE_URL)

redis = aioredis.from_url(settings.REDIS_URL)

async def get_database():
    return database

async def get_redis():
    return redis
