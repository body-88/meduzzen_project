from fastapi import APIRouter
from app.api.endpoints import user, auth

api_router = APIRouter()


api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(user.users_router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/user", tags=["user"])