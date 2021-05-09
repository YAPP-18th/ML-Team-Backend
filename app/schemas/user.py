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
    social_id: str
    nickname: str


class UserUpdate(UserBase):
    id: int
    pass


class UserResponse(UserBase):
    class Config:
        orm_mode = True
