from databases import Database
from app.models.user import User
from app.schemas.user import SignUpRequest, UserUpdateRequest, UserBase
from sqlalchemy import update, delete, select, insert
from app.db.db_settings import get_db
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from typing import List, Optional
from app.utils.hass_pass import get_hashed_password


class UserService:
    def __init__(self, db: Database):
        self.db = db


    async def get_user_by_email(self, email: str) -> Optional[UserBase]:
        query = select(User).where(User.user_email == email)
        return await self.db.fetch_one(query=query)
    
    
    async def create_user(self, user: SignUpRequest)-> User:
        hashed_password = get_hashed_password(user.user_password)
        existing_user = await self.get_user_by_email(email=user.user_email)
        if existing_user is not None:
            raise HTTPException(status_code=400, detail="Email already registered")
        query = insert(User).values(
            user_email=user.user_email,
            user_password=hashed_password,
            user_name=user.user_name,
            status=True,
        ).returning(User.id.label('user_id'), User.user_email, User.user_name, User.status, User.created_at)
        result = await self.db.fetch_one(query=query)
        return result
    
    
    async def get_user(self, user_id: int) -> User:
        query = select(User.id.label('user_id'), User.user_name, User.user_email, User.status).where(User.id == user_id)
        user = await self.db.fetch_one(query=query)
        if user is None:
            raise HTTPException(status_code=404, detail="User doesn't exist")
        return user


    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        query = select(User).offset(skip).limit(limit)
        result = await self.db.fetch_all(query=query)
        return result


    async def update_user(self, user_id: int, user: UserUpdateRequest) -> User:
        db_user = await self.get_user(user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User doesn't exist")
        if user.user_password:
            hashed_password = get_hashed_password(user.user_password)
            user_dict = user.dict(exclude_unset=True, exclude={"user_password_repeat"})
            user_dict["user_password"] = hashed_password
        else:
            user_dict = user.dict(exclude_unset=True, exclude={"user_password", "user_password_repeat"})
        query = (
            update(User)
            .where(User.id == user_id)
            .values(**user_dict)
            .returning(User.id.label('user_id'),User.user_password, User.user_name, User.description)
        )
        result = await self.db.fetch_one(query=query)
        return result


    async def delete_user(self, user_id: int) -> None:
        await self.get_user(user_id=user_id)
        query = delete(User).where(User.id == user_id)
        obj = await self.db.execute(query=query)
        return obj


async def get_user_service(db: Database = Depends(get_db)) -> UserService:
    return UserService(db)
