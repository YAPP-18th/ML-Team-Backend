import enum
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    id: Optional[int]
    provider: Optional[str]
    social_id: Optional[str]
    nickname: Optional[str]


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
                'nickname': 'new Nickname'
            }
        }


class UserResponse(UserBase):
    class Config:
        orm_mode = True
