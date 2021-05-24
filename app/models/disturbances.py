import enum

from sqlalchemy     import (
                        Column,
                        Enum,
                        Integer,
                        ForeignKey
                        )
from sqlalchemy.orm import relation

from app.database   import Base


class DistType(str, enum.Enum):
    SMARTPHONE = 'smartphone'
    AWAIT      = 'await'
    SLEEP      = 'sleep'


class Disturbances(Base):
    __tablename__ = 'disturbances'
    id            = Column('dis_id', Integer, primary_key=True, autoincrement=True)
    type          = Column('dis_type', Enum(DistType), nullable=False)
    count         = Column('dis_cnt', Integer, nullable=False)
    time          = Column('dis_time', Integer, nullable=False)
    my_study_id   = Column(Integer, ForeignKey('my_studies.id', ondelete='CASCADE'))
    report_id     = Column(Integer, ForeignKey('reports.id', ondelete='CASCADE'))
    # my_study      = relation('MyStudies', back_populates='disturbance')
    # report        = relation('Reports', back_populates='total_disturbance')
