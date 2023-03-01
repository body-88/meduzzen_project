from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class CustomBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        orm_mode = True

class UserBase(BaseModel):
    id: int
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: bool
    created_at: datetime
    updated_at: datetime
    description: Optional[str] = None


class SignInRequest(BaseModel):
    email: str
    password: str
    

class SignUpRequest(BaseModel):
    email: str
    password: str
    first_name: Optional[str]
    last_name: Optional[str]
    
    

class UserUpdateRequest(BaseModel):
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: bool
    description: Optional[str] = None


class UserInfo(BaseModel):
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]


class UsersListResponse(BaseModel):
    users: List[UserInfo]

class UserResponse(BaseModel):
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    description: Optional[str] = None