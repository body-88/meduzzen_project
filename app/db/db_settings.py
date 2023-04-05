import databases
import aioredis
from app.core.config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.CONTAINER_DB_PORT}/{settings.POSTGRES_DB}"
TEST_DB_URL = f"postgresql+asyncpg://{settings.TEST_POSTGRES_USER}:{settings.TEST_POSTGRES_PASSWORD}@{settings.TEST_POSTGRES_HOST}:{settings.CONTAINER_DB_PORT}/{settings.TEST_POSTGRES_DB}"
database = databases.Database(DATABASE_URL)

async def get_db():
    return database


if settings.ENVIRONMENT == "TESTING":
    REDIS_URL = settings.TEST_REDIS_URL
else:
    REDIS_URL = settings.REDIS_URL

async def get_redis():
    return await aioredis.from_url(REDIS_URL)
