from fastapi import APIRouter, Depends, Query
from app.schemas.user import SignUpRequest, UserResponse, UsersListResponse, UserUpdateRequest, Result, UserUpdateResponse
from app.servises.user import UserService, get_user_service

router = APIRouter()
users_router = APIRouter()


@users_router.get("", response_model=Result[UsersListResponse], status_code=200, response_description="Users returned")
async def read_users(service: UserService = Depends(get_user_service)) -> Result[UsersListResponse]:
    users = await service.get_users()
    return Result[UsersListResponse](result={"users":users})


@router.post("", response_model=Result[UserResponse], status_code=200, response_description="User created")
async def create_user(user: SignUpRequest,
                    service: UserService = Depends(get_user_service)) -> Result[UserResponse]:
    db_user = await service.create_user(user=user)
    return Result(result=UserResponse(**db_user))
    


@router.get("", response_model=Result[UserResponse], status_code=200, response_description="User returned")
async def read_user(user_id: int = Query(..., description="The ID of the user to retrieve"),
                    service: UserService = Depends(get_user_service)) -> Result[UserResponse]:
    db_user = await service.get_user(user_id=user_id)
    return Result[UserResponse](result=db_user)


@router.put("", response_model=Result[UserUpdateResponse], status_code=200, response_description="User updated")
async def update_user(user: UserUpdateRequest,
                    user_id: int = Query(..., description="The ID of the user to retrieve"),
                    service: UserService = Depends(get_user_service)) -> Result[UserUpdateResponse]:
    db_user = await service.update_user(user_id=user_id, user=user)
    return Result[UserUpdateResponse](result=db_user, message="User has been updated")


@router.delete("", status_code=200)
async def delete_user(user_id: int = Query(..., description="The ID of the user to delete"),
                    service: UserService = Depends(get_user_service)) -> Result:
    db_user = await service.delete_user(user_id=user_id)
    return Result(result=db_user, message="User deleted successfully")


