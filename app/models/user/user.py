<<<<<<< HEAD
import enum
from sqlalchemy import Column, Integer, Enum, String

from app.database.base_class import Base


class Provider(str, enum.Enum):
    GOOGLE = 'google'
    FACEBOOK = 'facebook'


class User(Base):
=======
from sqlalchemy     import Column, Integer, Float, Enum, String
from sqlalchemy.orm import relation

from app.database.base_class  import Base
from app.models.user.provider import Provider


class User(Base):
    __tablename__ = 'users'

>>>>>>> 1e939ba... 추가: Study Room
    id = Column('user_id', Integer, primary_key=True, autoincrement=True)
    provider = Column('user_provider', Enum(Provider), nullable=False)
    social_id = Column('user_social_id', String, nullable=False, unique=True)
    nickname = Column('user_nickname', String, nullable=False, unique=True)
<<<<<<< HEAD
=======

    study_rooms = relation('StudyRooms', back_populates = "owner")
>>>>>>> 1e939ba... 추가: Study Room
