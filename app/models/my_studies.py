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


class MyStudies(Base):
    __tablename__ = 'my_studies'
    id            = Column(Integer(), primary_key=True, autoincrement=True)
    date          = Column(Date, nullable=False)
    started_at    = Column(TIMESTAMP, nullable=False)
    ended_at      = Column(TIMESTAMP, nullable=False)
    total_time    = Column(Integer(), nullable=True)
    star_count    = Column(Integer(), nullable=True)
    disturbance   = Column(ARRAY(JSON), nullable=True)
    report_id     = Column(Integer(), ForeignKey('reports.id', ondelete='CASCADE'))
    study_room_id = Column(UUID(), ForeignKey('study_rooms.id', ondelete='CASCADE'))
    report        = relation('Reports', back_populates='my_studies')
    study_room    = relation('StudyRooms', back_populates='my_study')
