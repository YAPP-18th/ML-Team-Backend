import enum

from sqlalchemy     import (
                        Column,
                        Enum,
                        Integer,
                        SmallInteger,
                        ForeignKey
                        )
from sqlalchemy.orm import relation

from app.database   import Base


class Type(str, enum.Enum):
    SMARTPHONE = 'smartphone'
    AWAIT      = 'await'
    SLEEP      = 'sleep'


class Disturbances(Base):
    __tablename__ = 'disturbances'
    id            = Column(Integer(), primary_key=True, autoincrement=True)
    type          = Column(Enum(Type), nullable=False)
    count         = Column(SmallInteger(), nullable=False)
    time          = Column(SmallInteger(), nullable=False)
    my_study_id   = Column(Integer(), ForeignKey('my_studies.id', ondelete=True))
    report_id     = Column(Integer(), ForeignKey('reports.id', ondelete=True))
    my_study      = relation('MyStudies', back_populates='disturbance')
    report        = relation('Reports', back_populates='total_disturbance')