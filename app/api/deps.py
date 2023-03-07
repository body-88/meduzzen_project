from datetime import datetime
from fastapi import Depends, HTTPException, status
from app.core.config import settings
from app.servises.user import get_user_service, UserService

from jose import jwt
from pydantic import ValidationError
from app.schemas.user import UserResponse
from app.schemas.auth import TokenPayload
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

http_bearer = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer), service: UserService = Depends(get_user_service), ) -> UserResponse:
    try:
        payload = jwt.decode(credentials.credentials, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = await service.get_user(user_id = int(token_data.sub))
    
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return UserResponse(**user)