import secrets

from datetime import timedelta
from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    COMMON_API: str = '/api'
    PROJECT_NAME: str = "studeep"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SQLALCHEMY_DATABASE_URI: str = "postgresql://localhost:5432/studeep"

    class Config:
        env_file = ".env"


class DevelopSettings(BaseSettings):
    ALLOW_ORIGIN: list = ['*']
    ALLOW_CREDENTIAL: bool = False
    ALLOW_METHODS: list = ['*']
    ALLOW_HEADERS: list = ['*']
    ALLOW_HOST: list = ['*']
    ALLOW_EXPOSE_HEADERS: list = ['*']


class DeploySettings(BaseSettings):
    # TODO: 차후 배포 전 상세 설정 필요
    ALLOW_ORIGIN: list = ['https://studeep.com']
    ALLOW_CREDENTIAL: bool = True
    ALLOW_METHODS: list = ['*']
    ALLOW_HEADERS: list = ['*']
    ALLOW_HOST: list = ['*']
    ALLOW_EXPOSE_HEADERS: list = ['*']


class UserSettings(BaseSettings):
    API_USER: str = '/user'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


class StudyRoomSettings(BaseSettings):
    API_STUDY_ROOM: str = '/study-rooms'
    MIN_CAPACITY: int   = 0
    MAX_CAPACITY: int   = 5


class SocketSettings(BaseSettings):
    NAMESPACE_URL: str = '/study'


class TimeSettings(BaseSettings):
    KST = timedelta(hours=9)


common_settings      = CommonSettings()
develop_settings     = DevelopSettings()
deploy_settings      = DeploySettings()
user_settings        = UserSettings()
study_rooms_settings = StudyRoomSettings()
socket_settings      = SocketSettings()
time_settings        = TimeSettings()
