from pydantic   import BaseModel

from app.models import DisturbanceType


class DisturbanceBase(BaseModel):
    pass


class DisturbanceCreate(DisturbanceBase):
    type: DisturbanceType
    count: int
    time: int
    my_study_id: int
    report_id: int


class DisturbanceUpdate(DisturbanceBase):
    pass