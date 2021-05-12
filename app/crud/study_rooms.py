from uuid             import UUID
from typing           import Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm   import Session
from sqlalchemy.exc   import IntegrityError

from app.crud.base    import CRUDBase
from app.models       import StudyRooms
from app.schemas      import StudyRoomsCreate, StudyRoomsUpdate
from app.erros        import NoSuchElementException, InvalidArgumentException


def check_password_exist(room_info: Union[StudyRoomsCreate, StudyRoomsUpdate]):
    return False if (not room_info.is_public) and (not room_info.password) else True


class CRUDStudyRoom(CRUDBase[StudyRooms, StudyRoomsCreate, StudyRoomsUpdate]):
    def get(self, db: Session, room_id: UUID):
        try:
            data = db.query(self.model).filter(
                self.model.id == UUID(room_id)
            ).with_entities(
                self.model.id,
                self.model.title,
                self.model.description,
                self.model.is_public,
                self.model.current_join_counts,
                self.model.created_at,
                self.model.owner_id
            ).first()
            if data:
                return data
            else:
                raise NoSuchElementException(message='not found')

        except ValueError:
            raise NoSuchElementException(message='not found')


    def get_multi(self, db: Session, skip: int, limit: int, option: str):
        data = db.query(self.model).filter(
                self.model.current_join_counts < 5
            ).with_entities(
                self.model.id,
                self.model.title,
                self.model.description,
                self.model.is_public,
                self.model.current_join_counts,
                self.model.created_at,
                self.model.owner_id
            ).order_by(f'{option}').offset(skip).limit(limit).all()
        if data:
            return jsonable_encoder(data)
        else:
            raise NoSuchElementException(message='not found')


    def create(self, db: Session, room_info: StudyRoomsCreate):
        try:
            if not check_password_exist(room_info):
                raise InvalidArgumentException(message='filed required')

            room_info.current_join_counts += 1
            data = self.model(**jsonable_encoder(room_info))
            db.add(data)
            db.commit()

        except IntegrityError:
            raise NoSuchElementException(message='not found')


    def update(self, db: Session, room_id: str, room_info: StudyRoomsUpdate):
        try:
            if not check_password_exist(room_info):
                raise InvalidArgumentException(message='filed required')
                
            update_data = room_info.dict(exclude_none=True)
            data = db.query(self.model).filter(self.model.id == UUID(room_id)).update(update_data)
            if data:
                db.commit()
            else:
                raise NoSuchElementException(message='not found')    

        except ValueError:
            raise NoSuchElementException(message='not found')


    def remove(self, db: Session, room_id: str):
        try:
            data = db.query(self.model).filter(self.model.id == UUID(room_id)).first()
            if data:
                db.delete(data)
                db.commit()
            else:
                raise NoSuchElementException(message='not found')

        except ValueError:
            raise NoSuchElementException(message='not fund')


study_rooms = CRUDStudyRoom(StudyRooms)