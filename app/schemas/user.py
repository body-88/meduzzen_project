from typing import List, Optional
from pydantic import BaseModel, SecretStr
from datetime import datetime


class CustomBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        orm_mode = True

class UserBase(CustomBaseModel):
    id: int
    email: str
    password: SecretStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: Optional[bool] = None
    created_at: datetime
    updated_at: datetime
    description: Optional[str] = None


class SignInRequest(UserBase):
    email: str
    password: SecretStr
    

class SignUpRequest(UserBase):
    email: str
    password: SecretStr
    first_name: Optional[str]
    last_name: Optional[str] 
    

class UserUpdateRequest(UserBase):
    password: SecretStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: Optional[bool] = None
    description: Optional[str] = None


class UserId(UserBase):
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]


class UsersListResponse(UserBase):
    users: List[UserId]


class UserResponse(UserBase):
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: Optional[bool] = None
    created_at: datetime
    updated_at: datetime
    description: Optional[str] = None