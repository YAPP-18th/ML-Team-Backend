from uuid     import UUID
from typing   import Optional

from pydantic import BaseModel


class StudyRoomsBase(BaseModel):
    title: str
    description: str
    is_public: bool
    current_join_counts: int
    owner_id: int


class StudyRoomsCreate(StudyRoomsBase):
    password: Optional[str]
    current_join_counts: int = 0


class StudyRoomsUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    is_public: Optional[bool]
    password: Optional[str]


class StudyRoomResponse(StudyRoomsBase):
    data: Optional[list]
    message: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 'd7e3a12f-5669-4eb4-96db-b27efc6d96a2',
                'title': '주 4시간 이상 고시 공부방 🔥',
                'description': '같이 열심히 공부하실 분들만!',
                'is_public': False,
                'password': 'TestPassword!234',
                'current_join_counts': 1,
                'owner_id': 1
            }
        }