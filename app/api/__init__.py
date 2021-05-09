from fastapi import APIRouter

from app.api import users

user_router = APIRouter()

user_router.include_router(users.router, tags=["users"])
