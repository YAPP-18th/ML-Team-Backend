from uuid                           import uuid4
from datetime                       import datetime, timedelta

from sqlalchemy                     import Column, ForeignKey, String, Boolean, Integer, SmallInteger, DateTime
from sqlalchemy.orm                 import relation
from sqlalchemy.dialects.postgresql import UUID

from app.database.base_class        import Base


UTC_NOW = datetime.utcnow()
KST     = timedelta(hours=9)
KOR_NOW = UTC_NOW + KST


class StudyRooms(Base):
    __tablename__        = 'study_rooms'
    id                   = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title                = Column(String(64), nullable=False)
    description          = Column(String(256), nullable=False)
    is_public            = Column(Boolean(), default=False, nullable=False)
    password             = Column(String(32), nullable=True)
    current_join_counts  = Column(SmallInteger(), nullable=False, default=0)
    created_at           = Column(DateTime(), default=KOR_NOW)
    owner_id             = Column(Integer(), ForeignKey('users.user_id', ondelete='CASCADE'))
    owner                = relation('User', back_populates = "study_rooms")