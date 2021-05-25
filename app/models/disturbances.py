import enum

from sqlalchemy     import (
                        Column,
                        Enum,
                        Integer,
                        ForeignKey
                        )
from sqlalchemy.orm import relation

from app.database   import Base


class DisturbanceType(str, enum.Enum):
    SMARTPHONE = 'smartphone'
    AWAIT      = 'await'
    SLEEP      = 'sleep'


class Disturbances(Base):
    __tablename__ = 'disturbances'
    id            = Column('disturbance_id', Integer(), primary_key=True, autoincrement=True)
    type          = Column('disturbance_type', Enum(DisturbanceType), nullable=False)
    count         = Column('disturbance_count', Integer(), nullable=False)
    time          = Column('disturbance_time', Integer(), nullable=False)
    my_study_id   = Column(Integer(), ForeignKey('my_studies.my_study_id', ondelete=True))
    report_id     = Column(Integer(), ForeignKey('reports.report_id', ondelete=True))
    my_study      = relation('MyStudies', back_populates='disturbance')
    report        = relation('Reports', back_populates='total_disturbance')