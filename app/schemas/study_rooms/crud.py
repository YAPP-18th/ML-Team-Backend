from typing                import Optional

from pydantic              import BaseModel


class StudyRoomsBase(BaseModel):
    title: str
    description: str
    is_public: bool
    password: Optional[str]


class StudyRoomsCreate(StudyRoomsBase):
    current_join_counts: int = 0
    owner_id: int

    class Config:
        schema_extra = {
            'example': {
                'title': '주 4시간 이상 고시 공부방 🔥',
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
    password: Optional[str]