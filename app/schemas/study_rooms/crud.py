from typing     import Optional
from pydantic   import BaseModel
from datetime   import datetime

from app.models import Style


class StudyRoomsBase(BaseModel):
    password: Optional[str]


class StudyRoomsCreate(StudyRoomsBase):
    title: str
    description: Optional[str]
    style: Style
    is_public: bool
    current_join_counts: int = 0
    created_at: Optional[datetime]
    owner_id: int

    class Config:
        schema_extra = {
            'example': {
                'title': '주 4시간 이상 고시 공부방 🔥',
                'style': 'style_2',
                'description': '같이 열심히 공부하실 분들만!',
                'is_public': False,
                'password': 'TestPassword!234',
                'owner_id': 1
            }
        }


class StudyRoomsUpdate(StudyRoomsBase):
    title: Optional[str]
    description: Optional[str]
    is_public: Optional[bool]
    owner_id: int

    class Config:
        schema_extra = {
            'example': {
                'description': '매일 매일 캠 스터디 가능하신 분들만!',
                'is_public': False,
                'password': 'TestPassword!234',
                'owner_id': 1
            }
        } 


class StudyRoomJoin(StudyRoomsBase):
    user_id: int
    class Config:
        schema_extra = {
            'example': {
                'password': 'TestPassword!234'
            }
        } 