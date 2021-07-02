import traceback

from typing                  import Optional
from fastapi                 import (
                                APIRouter,
                                Depends,
                                status
                                )
from fastapi.responses       import JSONResponse
from sqlalchemy.orm.session  import Session

from app.api.deps            import get_db
from app.crud                import study_rooms
from app.schemas             import (
                                SuccessResponseBase,
                                ErrorResponseBase,
                                StudyRoomsCreate,
                                StudyRoomsUpdate,
                                StudyRoomJoin,
                                GetStudyRoomResponse,
                                GetStudyRoomsResponse,
                                NotFoundStudyRoomHandling,
                                NotFoundUserHandling,
                                PasswordNeedyStudyRoomHandling,
                                BodyNeedyStudyRoomHandling,
                                QueryNeedyStudyRoomHandling,
                                MethodNotAllowedHandling,
                                NoEmptyRoomHandling,
                                ForbiddenUserHandling,
                                ForbiddenPasswordHandling,
                                AlreadyJoinedHandling
                                )                                
from app.errors              import (
                                get_detail,
                                NoSuchElementException,
                                InvalidArgumentException,
                                RequestConflictException,
                                RequestInvalidException,
                                ForbiddenException
                                )


router = APIRouter()


@router.get(
    '/{room_id}',
    responses = {
        200: {
            "model": GetStudyRoomResponse,
            "description": "스터디룸 조회 성공"
        },
        500: {
            "model": ErrorResponseBase,
            "description": "서버에서 잡지 못한 에러"
        }
    }
)
def get_study_room(room_id: str, db: Session = Depends(get_db)):
    try:
        data = study_rooms.get(db, room_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content={'data': data})

    except NoSuchElementException:
        return JSONResponse(status_code=status.HTTP_200_OK, content={'data': []})

    except Exception as error:
        print(traceback.print_exc())
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'detail': f'server error: {error}'})
    
    finally:
        db.close()
        

@router.patch(
    '/{room_id}',
    responses = {
        200: {
            "model": SuccessResponseBase,
            "description": "스터디룸 수정 성공"
        },
        403: {
            "model": ForbiddenUserHandling,
            "description": "본인이 만들지 않은 방을 수정하려는 경우"
        },
        404: {
            "model": NotFoundStudyRoomHandling,
            "description": "수정을 시도한 스터디룸이 이미 존재하지 않는 경우"
        },
        405: {
            "model": MethodNotAllowedHandling,
            "description": "엔드포인트 경로에 스터디룸 아이디가 넘어오지 않을 경우"
        },
        422: {
            "model": PasswordNeedyStudyRoomHandling,
            "description": "비공개 스터디룸으로 설정하고 비밀번호를 입력하지 않은 경우"
        },
        500: {
            "model": ErrorResponseBase,
            "description": "서버에서 잡지 못한 에러"
        }
    }
)
def update_study_room(room_id: str, room_info: StudyRoomsUpdate, db: Session = Depends(get_db)):
    try:
        study_rooms.update(db, room_id, room_info)
        return JSONResponse(status_code=status.HTTP_200_OK, content={'data': ''})

    except ForbiddenException as forbidden_err:
        message = forbidden_err.message
        detail  = get_detail(param='database', field='user', message=message, err='invalid')
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': detail})

    except InvalidArgumentException as argument_err:
        message = argument_err.message
        detail  = get_detail(param='body', field='password', message=message, err='value_error')
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={'detail': detail})

    except NoSuchElementException as element_err:
        message = element_err.message
        detail  = get_detail(param='database', field='study room', message=message, err='database')
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': detail})

    except Exception as error:
        print(traceback.print_exc())
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'detail': f'server error: {error}'})


@router.delete(
    '/{room_id}',
    responses = {
        200: {
            "model": SuccessResponseBase,
            "description": "스터디룸 삭제 성공"
        },
        403: {
            "model": ForbiddenUserHandling,
            "description": "본인이 만들지 않은 방을 삭제하려는 경우"
        },
        404: {
            "model": NotFoundStudyRoomHandling,
            "description": "삭제를 시도한 스터디룸이 이미 존재하지 않는 경우"
        },
        405: {
            "model": MethodNotAllowedHandling,
            "description": "엔드포인트 경로에 스터디룸 아이디가 넘어오지 않을 경우"
        },        
        500: {
            "model": ErrorResponseBase,
            "description": "서버에서 잡지 못한 에러"
        }
    }
)
def delete_study_room(user_id: int, room_id: str, db: Session = Depends(get_db)):
    try:
        study_rooms.remove(db, room_id, user_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content={'data': ''})

    except ForbiddenException as forbidden_err:
        message = forbidden_err.message
        detail  = get_detail(param='database', field='user', message=message, err='invalid')
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': detail})

    except NoSuchElementException as element_err:
        message = element_err.message
        detail  = get_detail(param='database', field='study room', message=message, err='database')
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': detail})

    except Exception as error:
        print(traceback.print_exc())
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'detail': f'server error: {error}'})


@router.get(
    '',
    responses = {
        200: {
            "model": GetStudyRoomsResponse,
            "description": "스터디룸 조희 성공"
        },
        422: {
            "model": QueryNeedyStudyRoomHandling,
            "description": "쿼리 파라미터를 제대로 전달하지 않은 경우"
        },
        500: {
            "model": ErrorResponseBase,
            "description": "서버에서 잡지 못한 에러"
        }
    }
)
def get_study_rooms(
    skip: Optional[int] = None,
    limit: Optional[int] = None,
    owner_id: Optional[int] = None,
    option: Optional[str] = 'created_at',
    db: Session = Depends(get_db)
):
    try:
        data = study_rooms.get_multi(db, skip, limit, owner_id, option)
        return JSONResponse(status_code=status.HTTP_200_OK, content={'data': data})

    except NoSuchElementException:
        return JSONResponse(status_code=status.HTTP_200_OK, content={'data': []})

    except Exception as error:
        print(traceback.print_exc())
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'detail': f'server error: {error}'})


@router.post(
    '',
    responses = {
        200: {
            "model": SuccessResponseBase,
            "description": "스터디룸 생성 성공"
        },
        404: {
            "model": NotFoundUserHandling,
            "description": "방을 만드려는 사용자가 존재하지 않는 경우 (Postman 등을 통한 악용 방지)"
        },
        422: {
            "model": BodyNeedyStudyRoomHandling,
            "description": "제목, 설명과 같이 필요한 스터디룸 정보를 입력하지 않은 경우"
        },
        500: {
            "model": ErrorResponseBase,
            "description": "서버에서 잡지 못한 에러"
        }
    }
)
def create_study_room(room_info: StudyRoomsCreate, db: Session = Depends(get_db)):
    try:
        study_rooms.create(db, room_info)
        return JSONResponse(status_code=status.HTTP_200_OK, content={'data': ''})

    except InvalidArgumentException as argument_err:
        message = argument_err.message
        detail  = get_detail(param='body', field='password', message=message, err='value_error')
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={'detail': detail})        

    except NoSuchElementException as element_err:
        message = element_err.message
        detail  = get_detail(param='database', field='user', message='not found', err='database')
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': detail})

    except Exception as error:
        print(traceback.print_exc())
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'detail': f'server error: {error}'})


@router.post(
    '/{room_id}/join-check',
    responses = {
        200: {
            "model": SuccessResponseBase,
            "description": "스터디룸 생성 성공"
        },
        400: {
            "model": AlreadyJoinedHandling,
            "description": "이미 스터디룸에 접속했는데 접속 시도하는 경우"
        },
        403: {
            "model": ForbiddenPasswordHandling,
            "description": "비공개 방의 비밀번호 오입력 한 경우"
        },
        404: {
            "model": NotFoundStudyRoomHandling,
            "description": "존재하지 않는 방에 접근하려는 경우"
        },
        409: {
            "model": NoEmptyRoomHandling,
            "description": "이미 스터디룸의 참가 인원 수가 5명인 경우"
        },
        422: {
            "model": PasswordNeedyStudyRoomHandling,
            "description": "비공개 스터디룸일 때 비밀번호를 입력하지 않은 경우 \
                만약 공개된 스터디룸인데 비밀번호와 넘어올 경우 `msg` 부분에 `field not required` 반환"
        },
        500: {
            "model": ErrorResponseBase,
            "description": "서버에서 잡지 못한 에러"
        }
    }
)
def join_study_room(room_id: str, room_info: StudyRoomJoin, db: Session = Depends(get_db)):
    try:
        study_rooms.join(db, room_id, room_info)
        return JSONResponse(status_code=status.HTTP_200_OK, content={'data': ''})

    except RequestInvalidException as invalid_err:
        message = invalid_err.message
        detail  = get_detail(param='database', field='user', message=message, err='invalid')
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'detail': detail})

    except ForbiddenException as forbidden_err:
        message = forbidden_err.message
        detail  = get_detail(param='body', field='password', message=message, err='invalid')
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': detail})

    except NoSuchElementException as element_err:
        message = element_err.message
        detail  = get_detail(param='database', field='study room', message=message, err='database')
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': detail})

    except RequestConflictException as conflict_err:
        message = conflict_err.message
        detail  = get_detail(param='database', field='study room', message=message, err='database')
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'detail': detail})

    except InvalidArgumentException as argument_err:
        message = argument_err.message
        detail  = get_detail(param='body', field='password', message=message, err='value_error')
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={'detail': detail})        

    except Exception as error:
        print(traceback.print_exc())
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'detail': f'server error: {error}'})
