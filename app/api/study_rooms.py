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
                                GetStudyRoomResponse,
                                GetStudyRoomsResponse,
                                StudyRoomsCreate,
                                StudyRoomsUpdate
                                )


router = APIRouter()


@router.get('/{room_id}', response_model=GetStudyRoomResponse)
def get(room_id: str, db: Session = Depends(get_db)):
    data = get_study_room(db, room_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'detail': data})


@router.patch('/{room_id}', response_model=StudyRoomResponse)
def update(room_id: str, room_info: StudyRoomsUpdate, db: Session = Depends(get_db)):
    _ = update_study_room(db, room_id, room_info)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'detail': ''})


@router.delete('/{room_id}', response_model=StudyRoomResponse)
def delete(room_id: str, db: Session = Depends(get_db)):
    response = delete_study_room(db, room_id)
    return response
    

@router.get('', response_model=GetStudyRoomsResponse)
def get(skip: int, limit: int, option: str='created_at', db: Session = Depends(get_db)):
    data = get_study_rooms(db, skip, limit, option)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'detail': data})


@router.post('', response_model=StudyRoomResponse)
def create(rooms: StudyRoomsCreate, db: Session = Depends(get_db)):
    _ = create_study_room(db, rooms)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'detail': ''})