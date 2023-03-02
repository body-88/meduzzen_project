from fastapi import APIRouter, Depends

from app.schemas.user import SignUpRequest, UserResponse, UserUpdateRequest, UsersListResponse
from app.models.user import User
from app.servises.user import UserService, get_user_service

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=201, response_description="User created")
async def create_user(user: SignUpRequest, service: UserService = Depends(get_user_service)) -> UserResponse:
    db_user = await service.create_user(user=user)
    result = UserResponse(**db_user)
    return result


@router.get("/{user_id}", response_model=UserResponse, status_code=200, response_description="User returned")
async def read_user(user_id: int, service: UserService = Depends(get_user_service)) -> UserResponse:
    db_user = await service.get_user(user_id=user_id)
    return db_user


@router.put("/{user_id}", response_model=UserUpdateRequest, status_code=200, response_description="User updated")
async def update_user(user_id: int, user_info: UserUpdateRequest, service: UserService = Depends(get_user_service)) -> UserUpdateRequest:
    db_user = await service.get_user(user_id=user_id)
    result = await service.update_user(user_id=db_user.id, user=user_info)
    return result


@router.delete("/{user_id}", status_code=200)
async def delete_user(user_id: int, service: UserService = Depends(get_user_service)) -> dict:
    db_user = await service.get_user(user_id=user_id)
    db_user = await service.delete_user(user_id=user_id)
    return {"message" : "User deleted successfully"}


@router.get("/", response_model=UsersListResponse, status_code=200, response_description="Users returned")
async def read_users(service: UserService = Depends(get_user_service)) -> UsersListResponse:
    users = await service.get_users()
    return {"users": users}
