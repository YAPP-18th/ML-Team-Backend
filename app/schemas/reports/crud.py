from datetime import date
from pydantic import BaseModel


class ReportsBase(BaseModel):
    date: date
    user_id: int


class ReportsCreate(ReportsBase):
    pass


class ReportsUpdate(ReportsBase):
    pass