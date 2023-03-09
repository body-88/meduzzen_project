from datetime import datetime
from fastapi import Depends, HTTPException, status
from app.core.config import settings
from app.servises.user import get_user_service, UserService
from app.utils.auth0 import VerifyToken
from jose import jwt
from pydantic import ValidationError
from app.schemas.user import UserResponse, SignUpRequest
from app.schemas.auth import TokenPayload
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional


http_bearer = HTTPBearer()


async def get_current_user(token: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer),
                        service: UserService = Depends(get_user_service), ) -> Optional[UserResponse]:
    if token is None:
        return None

    try:
        payload = jwt.decode(token.credentials, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = await service.get_user_by_email(email = token_data.sub)
    
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )
    
        return UserResponse(**user)
    
    except (jwt.JWTError, ValidationError):
        pass
    
    try:
        verifier = VerifyToken(token.credentials)
        payload = verifier.verify()
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not verify credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = await service.get_user_by_email(email = payload["sub"])
        
        if user is None:
            user = SignUpRequest(
                user_email=payload.get('sub'),
                user_password=payload.get('sub'),
                user_password_repeat=payload.get('sub'),
                user_name=payload.get('sub')
            )
            user = await service.create_user(user=user)
        
        return UserResponse(**user)
    
    except Exception:
        pass

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )