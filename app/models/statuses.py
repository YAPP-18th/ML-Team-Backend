import enum

from sqlalchemy     import (
                        Column,
                        Enum,
                        Integer,
                        ForeignKey
                        )
from sqlalchemy.orm import relation

from app.database   import Base


class StatusType(str, enum.Enum):
    SMARTPHONE = 'smartphone'
    AWAIT      = 'await'
    SLEEP      = 'sleep'
    REST       = 'rest'


class Statuses(Base):
    __tablename__ = 'statuses'
    id            = Column('status_id', Integer(), primary_key=True, autoincrement=True)
    type          = Column('status_type', Enum(StatusType), nullable=False)
    count         = Column('status_count', Integer(), nullable=False)
    time          = Column('status_time', Integer(), nullable=False)
    my_study_id   = Column(Integer(), ForeignKey('my_studies.my_study_id', ondelete='CASCADE'))
    report_id     = Column(Integer(), ForeignKey('reports.report_id', ondelete='CASCADE'))
    my_study      = relation('MyStudies', back_populates='status')
    report        = relation('Reports', back_populates='total_status')