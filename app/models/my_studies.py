from sqlalchemy                     import (
                                        Column,
                                        Integer,
                                        ForeignKey,
                                        TIMESTAMP
                                        )
from sqlalchemy.orm                 import relation
from sqlalchemy.dialects.postgresql import UUID

from app.database                   import Base


class MyStudies(Base):
    __tablename__ = 'my_studies'
    id            = Column('my_study_id', Integer(), primary_key=True, autoincrement=True)
    started_at    = Column('my_study_started_at', TIMESTAMP, nullable=False)
    ended_at      = Column('my_study_ended_at', TIMESTAMP, nullable=True)
    total_time    = Column('my_study_total_time', Integer(), default=0, nullable=True)
    star_count    = Column('my_study_star_count', Integer(), nullable=True)
    report_id     = Column(Integer(), ForeignKey('reports.report_id', ondelete='CASCADE'))
    study_room_id = Column(UUID(as_uuid=True), ForeignKey('study_rooms.study_room_id', ondelete='CASCADE'))
    report        = relation('Reports', back_populates='my_studies')
    study_room    = relation('StudyRooms', back_populates='my_study')
    status        = relation('Statuses', back_populates='my_study')
