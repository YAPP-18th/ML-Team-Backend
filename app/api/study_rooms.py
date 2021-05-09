from fastapi                 import APIRouter, Depends, status
from fastapi.responses       import JSONResponse
from sqlalchemy.orm.session  import Session
from sqlalchemy.sql.sqltypes import JSON

from app.api.deps            import get_db
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
    data = get_study_room(db, room_id)
    if data:
        return JSONResponse(status_code=status.HTTP_200_OK, content={'data': data, 'message': ''})
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'data': data, 'message': 'NOT_FOUND'})


@router.patch('/{room_id}', response_model=StudyRoomResponse)
def update(room_id: str, room_info: StudyRoomsUpdate, db: Session = Depends(get_db)):
    response = update_study_room(db, room_id, room_info)
    return response


@router.delete('/{room_id}', response_model=StudyRoomResponse)
def delete(room_id: str, db: Session = Depends(get_db)):
    response = delete_study_room(db, room_id)
    return response
    

@router.get('', response_model=StudyRoomResponse)
def get(skip: int, limit: int, option: str='created_at', db: Session = Depends(get_db)):
    data = get_study_rooms(db, skip, limit, option)
    if data:
        return JSONResponse(status_code=status.HTTP_200_OK, content={'data': data, 'message': ''})
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'data': data, 'message': ''})


@router.post('', response_model=StudyRoomResponse)
def create(rooms: StudyRoomsCreate, db: Session = Depends(get_db)):
    data = create_study_room(db, rooms)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'data': '', 'message': ''})