import databases
import aioredis
from app.core.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

database = databases.Database(settings.DATABASE_URL)

engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True, echo=True)

Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

redis = aioredis.from_url(settings.REDIS_URL)

async def get_database():
    return database

async def get_redis():
    return redis

async def get_db_session():
    async with Session() as session:
        yield session

