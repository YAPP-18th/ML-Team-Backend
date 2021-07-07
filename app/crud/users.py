from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import User
from app.schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    # Declare model specific CRUD operation methods.
    def get_one_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.social_id == email).first()


users = CRUDUser(User)
