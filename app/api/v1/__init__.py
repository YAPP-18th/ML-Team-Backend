from fastapi    import APIRouter

from app.api.v1 import study_rooms

api_router = APIRouter()
api_router.include_router(study_rooms.router, prefix="/study-rooms", tags=["study_rooms"])
