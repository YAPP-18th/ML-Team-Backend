import enum

from datetime                       import datetime
from uuid                           import uuid4
from sqlalchemy                     import (
                                        Column,
                                        ForeignKey,
                                        String,
                                        Boolean,
                                        Integer,
                                        SmallInteger,
                                        DateTime,
                                        Enum
                                        )
from sqlalchemy.orm                 import relation
from sqlalchemy.dialects.postgresql import UUID

from app.database                   import Base


class Style(str, enum.Enum):
    STYLE_1 = 'style_1'
    STYLE_2 = 'style_2'
    STYLE_3 = 'style_3'
    STYLE_4 = 'style_4'


class StudyRooms(Base):
    __tablename__        = 'study_rooms'
    id                   = Column('study_room_id', UUID(as_uuid=True), primary_key=True, default=uuid4)
    title                = Column('study_room_title', String(64), nullable=False)
    style                = Column('study_room_style', Enum(Style), nullable=False)
    description          = Column('study_room_description', String(256), nullable=True)
    is_public            = Column('study_room_is_public', Boolean(), nullable=False)
    password             = Column('study_room_password', String(32), nullable=True)
    current_join_counts  = Column('study_room_current_join_counts', SmallInteger(), nullable=False, default=0)
    created_at           = Column('study_room_created_at', DateTime(), nullable=False)
    owner_id             = Column(Integer(), ForeignKey('users.user_id', ondelete='CASCADE'))
    owner                = relation('User', back_populates='study_rooms')
    my_study             = relation('MyStudies', back_populates='study_room')