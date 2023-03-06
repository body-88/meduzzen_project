from fastapi import APIRouter
from app.api.endpoints import user

api_router = APIRouter()


api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(user.users_router, prefix="/users", tags=["users"])