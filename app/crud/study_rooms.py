from uuid             import UUID
from typing           import Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm   import Session
from sqlalchemy.exc   import IntegrityError

from app.crud.base    import CRUDBase
from app.models       import StudyRooms
from app.schemas      import StudyRoomsCreate, StudyRoomsUpdate


def check_password_exist(room_info: Union[StudyRoomsCreate, StudyRoomsUpdate]):
    return False if (not room_info.is_public) and (not room_info.password) else True


class CRUDStudyRoom(CRUDBase[StudyRooms, StudyRoomsCreate, StudyRoomsUpdate]):
    def get(self, db: Session, room_id: UUID):
        try:
            study_room = db.query(self.model).filter(
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
            if study_room:
                return 'SUCCESS', jsonable_encoder(study_room)
            else:
                return 'NOT_FOUND_ROOM', None
        except ValueError:
            return 'NOT_FOUND_ROOM', None
        except Exception as error:
            print(error)
            print(error.__class__.__name__)
            return 'UNCAUGHT', None


    def get_multi(self, db: Session, skip: int, limit: int, option: str):
        try:
            study_rooms = db.query(self.model).filter(
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
            if study_rooms:
                return 'SUCCESS', jsonable_encoder(study_rooms)
            else:
                return 'NOT_FOUND_ROOM', None
        except Exception as error:
            print(error)
            print(error.__class__.__name__)
            return 'UNCAUGHT', None


    def create(self, db: Session, room_info: StudyRoomsCreate):
        try:
            if not check_password_exist(room_info):
                return 'PASSWORD', None
            room_info.current_join_counts += 1
            response = self.model(**jsonable_encoder(room_info))
            db.add(response)
            db.commit()
            return 'SUCCESS', None
        except IntegrityError:
            return 'NOT_FOUND_USER', None
        except Exception as error:
            print(error)
            print(error.__class__.__name__)
            return 'UNCAUGHT', None
    

    def update(self, db: Session, room_id: str, room_info: StudyRoomsUpdate):
        try:
            if not check_password_exist(room_info):
                return 'PASSWORD', None
            update_data = room_info.dict(exclude_none=True)
            study_room  = db.query(self.model).filter(self.model.id == UUID(room_id)).update(update_data)
            db.commit()
            return 'SUCCESS', study_room
        except ValueError:
            return 'NOT_FOUND_ROOM', None
        except Exception as error:
            print(error)
            print(error.__class__.__name__)
            return 'UNCAUGHT', None


    def remove(self, db: Session, room_id: str):
        try:
            study_room = db.query(self.model).filter(self.model.id == UUID(room_id)).first()
            if study_room:
                db.delete(study_room)
                db.commit()
                return 'SUCCESS', None
            else:
                return 'NOT_FOUND_ROOM', None
        except ValueError:
            return 'NOT_FOUND_ROOM', None
        except Exception as error:
            print(error)
            print(error.__class__.__name__)
            return 'UNCAUGHT', None


study_rooms = CRUDStudyRoom(StudyRooms)