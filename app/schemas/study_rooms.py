from uuid     import UUID
from typing   import Optional, Union

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


class StudyRoomsUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    is_public: Optional[bool]
    password: Optional[str]


class StudyRoomResponse(StudyRoomsBase):
    data: Union[list, dict, None]


class GetStudyRoomResponse(StudyRoomResponse):

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'title': '주 4시간 이상 고시 공부방 🔥',
                    'description': '같이 열심히 공부하실 분들만!',
                    'is_public': False,
                    'password': 'TestPassword!234',
                    'owner_id': 1
                }
            }
        }


class GetStudyRoomsResponse(StudyRoomsBase):

    class Config:
        schema_extra = {
            'example': {
                'data': [
                    {
                        "title": "스터디 룸 제목 수정",
                        "is_public": False,
                        "password": "Test!234",
                        "created_at": "2021-05-09T20:50:11.782727",
                        "description": "스터디룸 설명",
                        "id": "3d37627c-d87d-469e-8bf3-db7e796838cf",
                        "current_join_counts": 1,
                        "owner_id": 1
                    },
                    {
                        "title": "스터디룸 생성 제목",
                        "is_public": True,
                        "created_at": "2021-05-09T20:50:11.782727",
                        "description": "스터디룸 설명",
                        "id": "3b199025-92d7-4214-8f9c-b8224d81fca5",
                        "current_join_counts": 3,
                        "owner_id": 1
                    }
                ]
            }
        }


class CreateStudyRoomResponse(StudyRoomsBase):
    data: Optional[list]
    message: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'data': ''
            }
        }