from uuid import UUID

from typing import Optional

from pydantic       import BaseModel

class StudyRoomsBase(BaseModel):
    title: str
    description: str
    is_public: bool
    password: Optional[str]
    owner_id: int


class StudyRoomsCreate(StudyRoomsBase):
    title: str
    description: str
    is_public: bool
    owner_id: int


class StudyRoomsUpdate(StudyRoomsBase):
    pass


class StudyRoomResponse(StudyRoomsBase):
    class Config:
        orm_mode = True