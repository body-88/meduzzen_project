import databases
import aioredis
from app.core.config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.CONTAINER_DB_PORT}/{settings.POSTGRES_DB}"

database = databases.Database(DATABASE_URL)


async def get_db():
    return database

async def get_redis():
    return aioredis.from_url(settings.REDIS_URL)
