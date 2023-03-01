from databases import Database
from app.models.user import User
from app.schemas.user import SignUpRequest, UserUpdateRequest
from sqlalchemy import update, delete, select, insert
from app.db.db_settings import get_db
from fastapi import Depends, HTTPException


class UserService:
    def __init__(self, db: Database):
        self.db = db


    async def get_user_by_email(self, email: str):
        query = select(User).where(User.email == email)
        return await self.db.fetch_one(query=query)
    
    
    async def create_user(self, user: SignUpRequest):
        existing_user = await self.get_user_by_email(email=user.email)
        if existing_user is not None:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        query = insert(User).values(
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            status=True,
        ).returning(User.id, User.email, User.first_name, User.last_name, User.status, User.created_at)
        
        result = await self.db.fetch_one(query=query)
        return result
    
    
    async def get_user(self, user_id: int):
        query = select(User).where(User.id == user_id)
        user = await self.db.fetch_one(query=query)
        if user is None:
            raise HTTPException(status_code=404, detail="User doesn't exist")
        return user


    async def get_users(self, skip: int = 0, limit: int = 100):
        query = select(User).offset(skip).limit(limit)
        return await self.db.fetch_all(query=query)


    async def update_user(self, user_id: int, user: UserUpdateRequest):
        existing_user = await self.get_user(user_id=user_id)
        if existing_user is None:
            raise HTTPException(status_code=404, detail="User doesn't exist")
        query = (
            update(User)
            .where(User.id == user_id)
            .values(**user.dict(exclude_unset=True))
            .returning(User)
        )
        return await self.db.fetch_one(query=query)


    async def delete_user(self, user_id: int):
        query = delete(User).where(User.id == user_id)
        obj = await self.db.execute(query=query)
        return obj
    


async def get_user_service(db: Database = Depends(get_db)):
    return UserService(db)
