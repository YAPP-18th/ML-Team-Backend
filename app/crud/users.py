from sqlalchemy.orm   import Session
from fastapi.encoders import jsonable_encoder

from app.crud.base    import CRUDBase
from app.models       import User
from app.schemas      import UserCreate, UserUpdate
from app.errors       import NoSuchElementException


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get(self, db: Session, user_id: int):
        data = db.query(self.model).filter(
            self.model.id == user_id
        ).with_entities(
            self.model.id,
            self.model.nickname,
            self.model.provider,
            self.model.social_id
        ).first()

        if data:
            return jsonable_encoder(data)
        else:
            return NoSuchElementException(message='not found')


    def get_one_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.social_id == email).first()


users = CRUDUser(User)
