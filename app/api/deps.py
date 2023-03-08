from datetime import datetime
from fastapi import Depends, HTTPException, status
from app.core.config import settings
from app.servises.user import get_user_service, UserService
from app.utils.auth0 import VerifyToken
from jose import jwt
from pydantic import ValidationError
from app.schemas.user import UserMe
from app.schemas.auth import TokenPayload
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional
http_bearer = HTTPBearer()

async def get_current_user(token: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer), service: UserService = Depends(get_user_service), ) -> Optional[UserMe]:
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
    
        return UserMe(**user)
    
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
            user_dict={
                "user_email" : payload["sub"],
                "user_password" : payload["sub"],
                "user_name" : payload["sub"]
            }
            user = await service.create_user_auth0(user_dict=user_dict)
        
        return UserMe(**user)
    
    except Exception:
        pass

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )