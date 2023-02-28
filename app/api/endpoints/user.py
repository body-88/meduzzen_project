from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import user
from crud import crud_user
from db.db_settings import get_db
from models.user import User

router = APIRouter()

@router.post("/", response_model=user.UserResponse)
async def create_user(
user: user.SignUpRequest,
    db: Session = Depends(get_db),
) -> User:
    db_user = await crud_user.create_user(db=db, user=user)
    return db_user

@router.get("/{user_id}", response_model=user.UserResponse)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> User:
    db_user = await crud_user.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=user.UserResponse)
async def update_user(
    user_id: int,
    user_in: user.UserUpdateRequest,
    db: Session = Depends(get_db),
) -> User:
    db_user = await crud_user.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = await crud_user.update_user(db=db, user_id=db_user, user=user_in)
    return db_user

@router.delete("/{user_id}", response_model=user.UserResponse)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> User:
    db_user = await crud_user.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = await crud_user.delete_user(db=db, user_id=user_id)
    return db_user

@router.get("/", response_model=user.UsersListResponse)
async def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> user.UsersListResponse:
    users = await crud_user.get_users(db=db, skip=skip, limit=limit)
    return {"users": users}
