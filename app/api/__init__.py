from fastapi  import APIRouter

from app.api  import users, study_rooms
from app.core import study_rooms_settings


api_router = APIRouter()
api_router.include_router(
    users.router,
    tags=['users']
)
api_router.include_router(
    study_rooms.router,
    prefix=study_rooms_settings.API_STUDY_ROOM,
    tags=['study_rooms']
)
