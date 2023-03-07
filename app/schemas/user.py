from typing import List, Optional,  TypeVar, Generic
from pydantic import BaseModel, validator, Field
from datetime import datetime
from fastapi import HTTPException
from pydantic.generics import GenericModel


DataT = TypeVar('DataT')

class Result(GenericModel, Generic[DataT]):
    result: Optional[DataT]
    message: Optional[str] = None


class UserBase(BaseModel):
    user_id: int = Field(alias="id")
    user_email: str
    user_password: str
    user_password_repeat: str
    user_name: Optional[str]
    status: bool
    created_at: datetime
    updated_at: datetime
    description: Optional[str] = None

    class Config:
        orm_mode = True


class SignInRequest(BaseModel):
    user_email: str
    user_password: str
    user_password_repeat: str


    @validator('user_password_repeat')
    def passwords_match(cls, v, values, **kwargs):
        if 'user_password' in values and v != values['user_password']:
            raise ValueError('passwords do not match')
        return v
    
    @validator('user_password')
    def validate_password(cls, v):
        if len(v) < 4:
            raise HTTPException(status_code=422, detail="Password must be at least 4 characters long")
        return v
    
    
class SignUpRequest(BaseModel):
    user_email: str
    user_password: str
    user_password_repeat: str
    user_name: Optional[str]
    
    @validator('user_password_repeat')
    def passwords_match(cls, v, values, **kwargs):
        if 'user_password' in values and v != values['user_password']:
            raise ValueError('passwords do not match')
        return v
    
    @validator('user_password')
    def validate_password(cls, v):
        if len(v) < 4:
            raise HTTPException(status_code=422, detail="Password must be at least 4 characters long")
        return v
    
    

class UserUpdateRequest(BaseModel):
    user_password: Optional[str]
    user_password_repeat: Optional[str]
    user_name: Optional[str]
    description: Optional[str] = None

    @validator('user_password_repeat')
    def passwords_match(cls, v, values, **kwargs):
        if 'user_password' in values and v != values['user_password']:
            raise ValueError('passwords do not match')
        return v
    
    @validator('user_password')
    def validate_password(cls, v):
        if len(v) < 4:
            raise HTTPException(status_code=422, detail="Password must be at least 4 characters long")
        return v
    
    
class UserUpdateResponse(BaseModel):
    user_id: int
    user_name: Optional[str]    
    description: Optional[str] = None


class UserInfo(BaseModel):
    user_id: int = Field(alias="id")
    user_email: str
    user_name: Optional[str]

    class Config:
        orm_mode = True


class UsersListResponse(BaseModel):
    users: List[UserInfo]


class UserResponse(BaseModel):
    user_id: int 
    user_email: str
    user_name: Optional[str]
    status: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True