import secrets
from uuid import NAMESPACE_URL

from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    COMMON_API: str = '/api'
    PROJECT_NAME: str = "studeep"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SQLALCHEMY_DATABASE_URI: str = "postgresql://localhost:5432/studeep"

    class Config:
        env_file = ".env"


class UserSettings(BaseSettings):
    API_USER: str = '/user'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


class StudyRoomSettings(BaseSettings):
    API_STUDY_ROOM: str = '/study-rooms'


class SocketSettings(BaseSettings):
    NAMESPACE_URL: str = '/study'


common_settings      = CommonSettings()
user_settings        = UserSettings()
study_rooms_settings = StudyRoomSettings()
socket_settinngs     = SocketSettings()
