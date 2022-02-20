from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker

from app.core       import common_settings


engine       = create_engine(common_settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
