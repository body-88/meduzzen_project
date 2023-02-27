from app.models.user import User
from app.schemas.user import SignUpRequest, UserUpdateRequest
from app.db.db_settings import get_db
from sqlalchemy import update, delete, select

async def create_user(user: SignUpRequest):
    db = await get_db()
    query = User.__table__.insert().values(**user.dict())
    return await db.execute(query=query)


async def get_user(user_id: int):
    db = await get_db()
    query = select(User).where(User.id == user_id)
    return await db.fetch_one(query=query)


async def get_user_by_email(email: str):
    db = await get_db()
    query = select(User).where(User.email == email)
    return await db.fetch_one(query=query)


async def get_users(skip: int = 0, limit: int = 100):
    db = await get_db()
    query = select(User).offset(skip).limit(limit)
    return await db.fetch_all(query=query)


async def update_user(user_id: int, user: UserUpdateRequest):
    db = await get_db()
    query = (
        update(User)
        .where(User.id == user_id)
        .values(**user.dict(exclude_unset=True))
        .returning(User)
    )
    return await db.fetch_one(query=query)


async def delete_user(user_id: int):
    db = await get_db()
    query = delete(User).where(User.id == user_id)
    return await db.execute(query=query)
