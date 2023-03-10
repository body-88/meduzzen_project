from fastapi import APIRouter, Depends
from app.schemas.user import SignUpRequest, UserResponse, UsersListResponse, UserUpdateRequest, Result, UserUpdateResponse
from app.servises.user import UserService, get_user_service
from app.api.deps import get_current_user
from app.api.exceptions import raise_not_authenticated, wrong_account

router = APIRouter()
users_router = APIRouter()


@users_router.get("", response_model=Result[UsersListResponse], status_code=200, response_description="Users returned")
async def read_users(service: UserService = Depends(get_user_service), 
                    current_user: UserResponse = Depends(get_current_user)) -> Result[UsersListResponse]:
    if not current_user:
        raise_not_authenticated()
    users = await service.get_users()
    return Result[UsersListResponse](result={"users":users})


@router.post("", response_model=Result[UserResponse], status_code=200, response_description="User created")
async def create_user(user: SignUpRequest,
                    service: UserService = Depends(get_user_service)) -> Result[UserResponse]:
    db_user = await service.create_user(user=user)
    return Result(result=UserResponse(**db_user))
    

@router.get("/{user_id}", response_model=Result[UserResponse], status_code=200, response_description="User returned")
async def read_user(user_id: int,
                    service: UserService = Depends(get_user_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result[UserResponse]:
    if not current_user:
        raise_not_authenticated()
    db_user = await service.get_user(user_id=user_id)
    return Result[UserResponse](result=db_user)


@router.put("/{user_id}", response_model=Result[UserUpdateResponse], status_code=200, response_description="User updated")
async def update_user(user: UserUpdateRequest,
                    user_id: int,
                    service: UserService = Depends(get_user_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result[UserUpdateResponse]:
    if current_user.user_id != user_id:
        wrong_account()
    db_user = await service.update_user(user_id=user_id, user=user)
    return Result[UserUpdateResponse](result=db_user, message="User has been updated")


@router.delete("/{user_id}", status_code=200)
async def delete_user(user_id: int,
                    service: UserService = Depends(get_user_service),
                    current_user: UserResponse = Depends(get_current_user))-> Result:
    if current_user.user_id != user_id:
        wrong_account()
    db_user = await service.delete_user(user_id=user_id)
    return Result(result=db_user, message="Company deleted successfully")


