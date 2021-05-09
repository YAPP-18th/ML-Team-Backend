from uuid             import UUID
from typing           import Union

from fastapi          import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm   import Session

from app.crud.base    import CRUDBase
from app.models       import StudyRooms
from app.schemas      import StudyRoomsCreate, StudyRoomsUpdate


class StudyRoomCRUD(CRUDBase[StudyRooms, StudyRoomsCreate, StudyRoomsUpdate]):
    def get(self, db: Session, room_id: UUID):
        try:
            study_room = db.query(self.model).filter(StudyRooms.id == UUID(room_id)).first()
            return jsonable_encoder(study_room)
        except ValueError:

            return 'INVALID_UUID'
        except:
            return 'UNCAUGHT'


    def get_multi(self, db: Session, *, skip: int, limit: int, option: str):
        try:
            study_rooms = db.query(self.model).filter(
                    self.model.current_join_counts < 5
                ).order_by(f'{option}').offset(skip).limit(limit).all()
            if study_rooms:
                return jsonable_encoder(study_rooms)
            else:
                not_found_exception_handler()
        except:
            uncaught_exception_handler()


    def create(self, db: Session, *, obj_in: StudyRoomsCreate):
        return super().create(db, obj_in)
    

    def update(self, db: Session, *, room_id: str, room_info: StudyRoomsUpdate):
        try:
            password_exception_handler(room_info)
            update_data = room_info.dict(exclude_none=True)
            study_room  = db.query(StudyRooms).filter(StudyRooms.id == UUID(room_id)).update(update_data)
            db.commit()
            return study_room
        except ValueError:
            not_found_exception_handler()
        except:
            uncaught_exception_handler()


    def remove(self, db: Session, *, room_id: str):
        try:
            study_room = db.query(StudyRooms).filter(StudyRooms.id == UUID(room_id)).first()
            if study_room:
                db.delete(study_room)
                db.commit()
            else:
                not_found_exception_handler()
        except ValueError:
            not_found_exception_handler()
        except:
            uncaught_exception_handler()
  


         
def create_study_room(db: Session, room_info: StudyRoomsCreate):
    password_exception_handler(room_info)
    room_info.current_join_counts += 1
    response = StudyRooms(**jsonable_encoder(room_info))
    db.add(response)
    db.commit()
    return response


def update_study_room(db: Session, room_id: str, room_info: StudyRoomsUpdate):
    try:
        password_exception_handler(room_info)
        update_data = room_info.dict(exclude_none=True)
        study_room  = db.query(StudyRooms).filter(StudyRooms.id == UUID(room_id)).update(update_data)
        db.commit()
        return study_room
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')


def delete_study_room(db: Session, room_id: str):
    try:
        study_room = db.query(StudyRooms).filter(StudyRooms.id == UUID(room_id)).first()
        if study_room:
            db.delete(study_room)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')

        