import secrets

from pydantic import BaseSettings


<<<<<<< HEAD
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    API_USER: str = "/api/user"
    PROJECT_NAME: str = "FastAPI"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SQLALCHEMY_DATABASE_URI: str = "postgresql://localhost:5432/fastapi_db"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
=======
class CommonSettings(BaseSettings):
    COMMON_API: str = '/api'
    PROJECT_NAME: str = "studeep"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SQLALCHEMY_DATABASE_URI: str = "postgresql://localhost:5432/studeep"
>>>>>>> 15048eb... 수정: 전체적인 폴더 구조 리팩토링

    class Config:
        env_file = ".env"


class StudyRoomSettings(BaseSettings):
    API_STUDY_ROOM: str = '/study-rooms'


common_settings      = CommonSettings()
study_rooms_settings = StudyRoomSettings()
