from pydantic   import BaseModel

from app.models import StatusType


class StatusBase(BaseModel):
    pass


class StatusCreate(StatusBase):
    type: StatusType
    count: int
    time: int
    my_study_id: int
    report_id: int


class StatusUpdate(StatusBase):
    pass