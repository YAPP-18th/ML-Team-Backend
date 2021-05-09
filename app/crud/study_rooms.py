from uuid                    import UUID
from typing                  import Union

from fastapi                 import HTTPException, status
from fastapi.encoders        import jsonable_encoder
from sqlalchemy.orm          import Session

from app.models              import StudyRooms
from app.schemas             import StudyRoomsCreate, StudyRoomsUpdate


def password_exception_handler(room_info: Union[StudyRoomsCreate, StudyRoomsUpdate]):
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


def get_study_room(db: Session, room_id: str):
    try: 
        study_room = db.query(StudyRooms).filter(StudyRooms.id == UUID(room_id)).first()
        if study_room:
            return jsonable_encoder(study_room)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='ROOM_ID_ERROR')

        
def get_study_rooms(db: Session, skip: int, limit: int, option: str):
    study_rooms = db.query(StudyRooms).filter(StudyRooms.current_join_counts < 5).order_by(f'{option}').offset(skip).limit(limit).all()
    if study_rooms:
        return jsonable_encoder(study_rooms)
    
 
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
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='ROOM_ID_ERROR')


def delete_study_room(db: Session, room_id: str):
    try:
        study_room = db.query(StudyRooms).filter(StudyRooms.id == UUID(room_id)).first()
        if study_room:
            db.delete(study_room)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='ROOM_ID_ERROR')

        