import secrets

from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    COMMON_API: str = '/api'
    PROJECT_NAME: str = "studeep"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SQLALCHEMY_DATABASE_URI: str = "postgresql://localhost:5432/studeep"

    class Config:
        env_file = ".env"


class StudyRoomSettings(BaseSettings):
    API_STUDY_ROOM: str = '/study-rooms'


common_settings      = CommonSettings()
study_rooms_settings = StudyRoomSettings()
