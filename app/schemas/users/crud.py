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

    class Config:
        schema_extra = {
            'example': {
                'provider': 'google',
                'nickname': 'Studeep_User'
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
                    'MON': 2,
                    'TUE': 2,
                    'WED': 2,
                    'THU': 2,
                    'FRI': 2,
                    'SAT': 2,
                    'SUN': 2
                }
            }
        }
