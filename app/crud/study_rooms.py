from uuid                    import UUID
from typing                  import TypeVar

from fastapi                 import HTTPException, status
from fastapi.encoders        import jsonable_encoder
from pydantic                import BaseModel
from sqlalchemy.orm          import Session

from app.models              import StudyRooms
from app.schemas             import StudyRoomsCreate, StudyRoomsUpdate
from app.erros.study_rooms.handling import CustomException, NotFoundHandler


ModelSchema = TypeVar('ModelSchema', bound=BaseModel)


def password_exception_handler(room_info: ModelSchema):
    detail = [
        {
            "loc": [
                "body",
                "password"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
    if (not room_info.is_public) and (not room_info.password):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)
    else:
        pass


def get_study_room(db: Session, room_id: str):
    study_room = db.query(StudyRooms).filter(StudyRooms.id == UUID(room_id)).first()
    if study_room:
        return study_room

        

def get_study_rooms(db: Session, skip: int, limit: int, option: str):
    study_rooms = db.query(StudyRooms).filter(StudyRooms.current_join_counts < 5).order_by(f'{option}').offset(skip).limit(limit).all()
    return study_rooms
 

def create_study_room(db: Session, room_info: StudyRoomsCreate):
    print(room_info.is_public)
    password_exception_handler(StudyRoomsCreate)
    room_info.current_join_counts += 1
    response = StudyRooms(**jsonable_encoder(room_info))
    db.add(response)
    db.commit()
    return response


def update_study_room(db: Session, room_id: str, room_info: StudyRoomsUpdate):
    password_exception_handler(StudyRoomsUpdate)
    update_data = room_info.dict(exclude_none=True)
    study_room  = db.query(StudyRooms).filter(StudyRooms.id == UUID(room_id)).update(update_data)
    db.commit()
    return study_room


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
        