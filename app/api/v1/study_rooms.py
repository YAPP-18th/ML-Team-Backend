from fastapi                 import APIRouter, Depends
from sqlalchemy.orm.session  import Session

from app.api.deps            import get_db
from app.erros.study_rooms   import CustomException
from app.crud                import (
                                get_study_room,
                                get_study_rooms,
                                create_study_room,
                                update_study_room,
                                delete_study_room
                                )
from app.schemas             import (
                                StudyRoomResponse,
                                StudyRoomsCreate,
                                StudyRoomsUpdate
                                )



router = APIRouter()


@router.get('/{room_id}', response_model=StudyRoomResponse)
def get(room_id: str, db: Session = Depends(get_db)):
    study_room = get_study_room(db, room_id)
    if study_room:
        return study_room
    else:
        raise CustomException(message = 'NOT_FOUND')


@router.patch('/{room_id}')
def update(room_id: str, room_info: StudyRoomsUpdate, db: Session = Depends(get_db)):
    response = update_study_room(db, room_id, room_info)
    return response


@router.delete('/{room_id}')
def delete(room_id: str, db: Session = Depends(get_db)):
    _ = delete_study_room(db, room_id)
    

@router.get('')
def get(skip: int, limit: int, option: str='created_at', db: Session = Depends(get_db)):
    response = get_study_rooms(db, skip, limit, option)
    return response


@router.post('')
def create(rooms: StudyRoomsCreate, db: Session = Depends(get_db)):
    create_study_room(db, rooms)