from sqlalchemy     import (
                        Column,
                        ForeignKey,
                        Integer,
                        Date
                        )
from sqlalchemy.orm import relation

from app.database   import Base


class Reports(Base):
    __tablename__     = 'reports'
    id                = Column('report_id', Integer(), primary_key=True, autoincrement=True)
    date              = Column('report_date', Date, nullable=False)
    achievement       = Column('report_achievement', Integer(), nullable=True)
    concentration     = Column('report_concentration', Integer(), nullable=True)
    total_time        = Column('report_total_time', Integer(), default=0, nullable=True)
    total_star_count  = Column('report_total_star_count', Integer(), default=0, nullable=True)
    user_id           = Column(Integer(), ForeignKey('users.user_id', ondelete='CASCADE'))
    user              = relation('User', back_populates='reports')
    my_studies        = relation('MyStudies', back_populates='report')
    total_status      = relation('Statuses', back_populates='report')
