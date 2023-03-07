from fastapi import status, HTTPException, Depends, APIRouter
from app.schemas.user import SignInRequest, UserResponse
from app.schemas.auth import TokenSchema
from app.utils.hass_pass import verify_password
from app.servises.jwt_service import create_access_token, create_refresh_token
from app.servises.user import UserService, get_user_service

from app.api.deps import get_current_user


router = APIRouter()

@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: SignInRequest = Depends(), service: UserService = Depends(get_user_service)):
    user = await service.get_user_by_email(email=form_data.user_email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_password = user['user_password']
    if not verify_password(form_data.user_password,  hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_access_token(user['id']),
        "refresh_token": create_refresh_token(user['id']),
    }
    


@router.get('/me', summary='Get details of currently logged in user', response_model=UserResponse)
async def get_me(user = Depends(get_current_user)):
    return user