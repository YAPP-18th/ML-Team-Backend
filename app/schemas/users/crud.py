import enum
import json
from typing import Optional

from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import JSON


class UserBase(BaseModel):
    id: Optional[int]
    provider: Optional[str]
    social_id: Optional[str]
    nickname: Optional[str]
    goal: Optional[dict]


class UserCreate(UserBase):
    provider: str
    nickname: str
    goal: dict

    class Config:
        schema_extra = {
            'example': {
                'provider': 'google',
                'nickname': 'Studeep_User',
                'goal': {
                    '월': 2,
                    '화': 2,
                    '수': 2,
                    '목': 2,
                    '금': 2,
                    '토': 2,
                    '일': 2
                }
            }
        }


class UserUpdate(UserBase):
    id: int
    pass

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'provider': 'google',
                'social_id': 'example@gmail.com',
                'nickname': 'new Nickname',
                'goal': {
                    '월': 2,
                    '화': 2,
                    '수': 2,
                    '목': 2,
                    '금': 2,
                    '토': 2,
                    '일': 2
                }
            }
        }


class UserResponse(UserBase):
    class Config:
        orm_mode = True
