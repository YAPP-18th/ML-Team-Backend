from datetime       import datetime
from sqlalchemy     import (
                        Column,
                        ForeignKey,
                        Integer,
                        Date
                        )
from sqlalchemy.orm import relation

from app.database   import Base
from app.core       import time_settings


KOR_NOW  = datetime.utcnow() + time_settings.KST

if (KOR_NOW.hour >= 00) and (KOR_NOW.hour < 5):
    KOR_DATE = datetime(KOR_NOW.year, KOR_NOW.month, KOR_NOW.day - 1)
else:
    KOR_DATE = datetime(KOR_NOW.year, KOR_NOW.month, KOR_NOW.day)


class Reports(Base):
    __tablename__     = 'reports'
    id                = Column(Integer(), primary_key=True, autoincrement=True)
    date              = Column(Date, default=KOR_DATE, nullable=False)
    achievement       = Column(Integer(), nullable=True)
    concentration     = Column(Integer(), nullable=True)
    total_time        = Column(Integer(), nullable=True)
    total_star_count  = Column(Integer(), nullable=True)
    user_id           = Column(Integer(), ForeignKey('users.user_id', ondelete='CASCADE'))
    user              = relation('User', back_populates='reports')
    my_studies        = relation('MyStudies', back_populates='report')
    total_disturbance = relation('Disturbances', back_populates='report')
