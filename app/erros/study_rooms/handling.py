from typing             import Union

from fastapi            import status
from fastapi.exceptions import HTTPException

from app.schemas        import StudyRoomsCreate, StudyRoomsUpdate
from app.erros.handling import get_detail


def password_exception_handler(room_info: Union[StudyRoomsCreate, StudyRoomsUpdate]):
    detail = get_detail(param='body', field='password', err='value_error')
    if (not room_info.is_public) and (not room_info.password):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


def invalid_uuid_exception_handler():
    pass

