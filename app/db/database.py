import databases
import sqlalchemy
import aioredis
from app.core.config import settings
from sqlalchemy.orm import sessionmaker

database = databases.Database(settings.DATABASE_URL)

engine = sqlalchemy.create_engine(settings.DATABASE_URL)

Session = sessionmaker(engine, autocommit=False, autoflush=False)

redis = aioredis.from_url(settings.REDIS_URL)


async def connect_db():
    await database.connect()
    return database


async def close_db(database: databases.Database):
    await database.disconnect()


def get_db():
    try:
        db = engine.connect()
        yield db
    finally:
        db.close()


async def get_redis():
    return redis