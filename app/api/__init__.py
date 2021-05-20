from fastapi     import APIRouter, Depends

from app.api     import users, study_rooms
from app.core    import study_rooms_settings, user_settings
from app.service import auth_token


api_router = APIRouter()
api_router.include_router(
    users.router,
    prefix=user_settings.API_USER,
    tags=['users']
)
# TODO: 의존성 추가
api_router.include_router(
    study_rooms.router,
    prefix=study_rooms_settings.API_STUDY_ROOM,
    # dependencies=[Depends(auth_token),],
    tags=['study_rooms']
)