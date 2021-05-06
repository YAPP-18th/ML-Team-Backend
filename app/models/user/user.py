from sqlalchemy import Column, Integer, Float, Enum, String

from app.database.base_class import Base
from app.models.user.provider import Provider


class User(Base):
    id = Column('user_id', Integer, primary_key=True, autoincrement=True)
    provider = Column('user_provider', Enum(Provider), nullable=False)
    social_id = Column('user_social_id', String, nullable=False, unique=True)
    nickname = Column('user_nickname', String, nullable=False, unique=True)