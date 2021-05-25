from uuid     import UUID
from datetime import date, datetime
from typing   import Optional
from pydantic import BaseModel


class MyStudiesBase(BaseModel):
    pass


class MyStudiesCreate(MyStudiesBase):
    date: date
    report_id: int
    study_room_id: UUID

    class config:
        schema_extra = {

        }


class MyStudiesUpdate(MyStudiesBase):
    total_time: int
    ended_at: datetime