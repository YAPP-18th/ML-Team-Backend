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
    ALLOW_ORIGIN: list = [
        'https://www.studeep.com/',
        'https://api.studeep.com/',
        'https://studeep.com/',
        'http://localhost/',
        'http://localhost:3000/',
        'http://localhost:8000/'
    ]
    ALLOW_CREDENTIAL: bool = True
    ALLOW_METHODS: list = ['*']
    ALLOW_HEADERS: list = ['*']
    ALLOW_HOST: list = ['*']
    ALLOW_EXPOSE_HEADERS: list = ['*']


class DeploySettings(BaseSettings):
    ALLOW_ORIGIN: list = [
        # 'https://www.studeep.com/',
        # 'https://api.studeep.com/',
        # 'https://studeep.com/',
        # 'http://localhost/',
        # 'http://localhost:3000/',
        # 'http://localhost:8000/'
        '*'
    ]
    ALLOW_CREDENTIAL: bool = True
    ALLOW_METHODS: list = ['*']
    ALLOW_HEADERS: list = ['*']
    ALLOW_HOST: list = ['*.studeep.com', 'localhost']
    ALLOW_EXPOSE_HEADERS: list = ['Authorization', 'authorization']


class UserSettings(BaseSettings):
    API_USER: str = '/user'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 300000


class StudyRoomSettings(BaseSettings):
    API_STUDY_ROOM: str = '/study-rooms'
    MIN_CAPACITY: int   = 0
    MAX_CAPACITY: int   = 5


class MyStudySettings(BaseSettings):
    API_MY_STUDY: str = '/my-studies'


class ReportSettings(BaseSettings):
    API_REPORT: str = '/reports'


class SocketSettings(BaseSettings):
    NAMESPACE_URL: str = '/study'


class TimeSettings(BaseSettings):
    KST = timedelta(hours=9)

class RedisSettings(BaseSettings):
    HOST = "27.96.131.49"
    PORT = 6000


common_settings      = CommonSettings()
develop_settings     = DevelopSettings()
deploy_settings      = DeploySettings()
user_settings        = UserSettings()
study_rooms_settings = StudyRoomSettings()
my_studies_settings  = MyStudySettings()
report_settings      = ReportSettings()
socket_settings      = SocketSettings()
time_settings        = TimeSettings()
redis_settings       = RedisSettings()
