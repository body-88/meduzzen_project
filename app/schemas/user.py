from typing import List, Optional
from pydantic import BaseModel, SecretStr
from datetime import datetime


class UserBase(BaseModel):
    id: int
    email: str
    password: SecretStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: Optional[bool] = None
    created_at: datetime
    updated_at: datetime
    description: Optional[str] = None


class SignInRequest(BaseModel):
    email: str
    password: SecretStr
    

class SignUpRequest(BaseModel):
    email: str
    password: SecretStr
    first_name: Optional[str]
    last_name: Optional[str] 
    

class UserUpdateRequest(BaseModel):
    password: SecretStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: Optional[bool] = None
    description: Optional[str] = None


class UserId(BaseModel):
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]


class UsersListResponse(BaseModel):
    users: List[UserId]


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: Optional[bool] = None
    created_at: datetime
    updated_at: datetime
    description: Optional[str] = None