from uuid             import UUID
from typing           import Union, Optional
from datetime         import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy       import and_
from sqlalchemy.orm   import Session
from sqlalchemy.exc   import IntegrityError

from app.core         import study_rooms_settings
from app.crud.base    import CRUDBase
from app.models       import StudyRooms
from app.schemas      import (
                        StudyRoomsCreate,
                        StudyRoomsUpdate,
                        StudyRoomJoin
                        )
from app.errors       import (
                        NoSuchElementException,
                        InvalidArgumentException,
                        RequestConflictException,
                        ForbiddenException
                        )
from app.core         import time_settings


MAX_CAPACITY = study_rooms_settings.MAX_CAPACITY


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
                self.model.style,
                self.model.description,
                self.model.is_public,
                self.model.current_join_counts,
                self.model.created_at,
                self.model.owner_id
            ).first()

            if data:
                return jsonable_encoder(data)
            else:
                raise NoSuchElementException(message='not found')

        except ValueError:
            raise NoSuchElementException(message='not found')


    def get_multi(
        self,
        db: Session,
        skip: Optional[int],
        limit: Optional[int],
        owner_id: Optional[int],
        option: Optional[str]
    ):
        query = db.query(self.model)
        if owner_id:
            query = query.filter(self.model.owner_id == owner_id)

        data = query.filter(
                self.model.current_join_counts < MAX_CAPACITY
            ).with_entities(
                self.model.id,
                self.model.title,
                self.model.style,
                self.model.description,
                self.model.is_public,
                self.model.current_join_counts,
                self.model.created_at,
                self.model.owner_id
            ).order_by(f'study_room_{option}').offset(skip).limit(limit).all()

        if data:
            return jsonable_encoder(data)
        else:
            raise NoSuchElementException(message='not found')


    def create(self, db: Session, room_info: StudyRoomsCreate):
        try:
            if not check_password_exist(room_info):
                raise InvalidArgumentException(message='field required')

            room_info.current_join_counts += 1
            room_info.created_at           = datetime.utcnow() + time_settings.KST
            data = self.model(**jsonable_encoder(room_info))
            db.add(data)
            db.commit()

        except IntegrityError:
            raise NoSuchElementException(message='not found')


    def update(self, db: Session, room_id: str, room_info: StudyRoomsUpdate):
        try:
            if not check_password_exist(room_info):
                raise InvalidArgumentException(message='field required')
                
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
            raise NoSuchElementException(message='not found')


    def join(self, db: Session, room_id: str, room_info: StudyRoomJoin):
        try:
            if not room_id:
                raise NoSuchElementException(message='not found')
            data = db.query(self.model).filter(self.model.id == UUID(room_id)).first()
            study_room = jsonable_encoder(data)
            if study_room:
                if study_room['current_join_counts'] >= MAX_CAPACITY:
                    raise RequestConflictException(message='no empty')
                
                if study_room['is_public']:
                   if room_info.password:
                       raise InvalidArgumentException(message='field not required')
                else:
                    if not room_info.password:
                        raise InvalidArgumentException(message='field required')
                    elif room_info.password != study_room['password']:
                        raise ForbiddenException(message='forbidden')

                data.current_join_counts += 1
                db.commit()

            else:
                raise NoSuchElementException(message='not found')

        except ValueError:
            raise NoSuchElementException(message='not found')

        finally:
            db.close()


    def leave(self, db: Session, room_id: str):
        try: 
            db.query(self.model).filter(self.model.id == UUID(room_id)).update(
                {'current_join_counts': self.model.current_join_counts  - 1} 
            )
            db.commit()
            return 'room leaved'

        except Exception as error:
            # TODO: 더 구체적인 에러 핸들링 필요 ex. Positive Integer(MIN_CAPACITY)
            return error

        finally:
            db.close()


study_rooms = CRUDStudyRoom(StudyRooms)