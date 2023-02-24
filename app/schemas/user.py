from typing import List, Optional
from pydantic import BaseModel
from models.user import User

class SignInRequest(BaseModel):
    email: str
    password: str


class SignUpRequest(BaseModel):
    email: str
    password: str
    full_name: Optional[str]


class UserUpdateRequest(BaseModel):
    email: Optional[str]
    password: Optional[str]
    full_name: Optional[str]


class UsersListResponse(BaseModel):
    users: List[User]