from sqlalchemy     import (
                        Column,
                        ForeignKey,
                        Integer,
                        Date,
                        ARRAY,
                        JSON
                        )
from sqlalchemy.orm import relation

from app.database   import Base


class Reports(Base):
    __tablename__     = 'reports'
    id                = Column(Integer(), primary_key=True, autoincrement=True)
    date              = Column(Date, nullable=False)
    achivement        = Column(Integer(), nullable=False)
    concentration     = Column(Integer(), nullable=False)
    total_time        = Column(Integer(), nullable=False)
    total_star_count  = Column(Integer(), nullable=False)
    total_disturbance = Column(ARRAY(JSON), nullable=True)
    user_id           = Column(Integer(), ForeignKey('users.user_id', ondelete='CASCADE'))
    user              = relation('User', back_populates='reports')
    my_studies        = relation('MyStudies', back_populates='report')