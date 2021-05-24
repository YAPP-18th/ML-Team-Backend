from datetime                       import datetime, timedelta
from sqlalchemy                     import (
                                        Column,
                                        Integer,
                                        ForeignKey,
                                        Date,
                                        ARRAY,
                                        JSON,
                                        TIMESTAMP
                                        )
from sqlalchemy.orm                 import relation
from sqlalchemy.dialects.postgresql import UUID

from app.database                   import Base


UTC_NOW = datetime.utcnow()
KST     = timedelta(hours=9)
KOR_NOW = UTC_NOW + KST


class MyStudies(Base):
    __tablename__ = 'my_studies'
    id            = Column(Integer(), primary_key=True, autoincrement=True)
    started_at    = Column(TIMESTAMP, default=KOR_NOW, nullable=False)
    ended_at      = Column(TIMESTAMP, nullable=True)
    total_time    = Column(Integer(), nullable=True)
    star_count    = Column(Integer(), nullable=True)
    report_id     = Column(Integer(), ForeignKey('reports.id', ondelete='CASCADE'))
    study_room_id = Column(UUID(), ForeignKey('study_rooms.id', ondelete='CASCADE'))
    report        = relation('Reports', back_populates='my_studies')
    study_room    = relation('StudyRooms', back_populates='my_study')
    disturbance   = relation('Disturbances', back_populates='my_study')
