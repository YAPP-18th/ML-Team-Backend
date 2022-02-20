import traceback

from fastapi                import (
                                APIRouter,
                                Depends,
                                status
                                )
from fastapi.responses      import JSONResponse
from sqlalchemy.orm.session import Session

from app.api.deps           import get_db
from app.crud               import my_studies
from app.schemas            import (
                                ErrorResponseBase,
                                GetMyStudiesResponse,
                                NotFoundMyStudiesHandling
                                )
from app.errors             import (
                                get_detail,
                                NoSuchElementException
                                )


router = APIRouter()


@router.get(
    '',
    responses = {
        200: {
            "model": GetMyStudiesResponse,
            "description": "마이스터디 조회 성공"
        },
        500: {
            "model": ErrorResponseBase,
            "description": "서버에서 잡지 못한 에러"
        }
    }
)
def get_my_studies(date: str, user_id: int, db: Session = Depends(get_db)):
    try:
        data = my_studies.get(db, date, user_id)
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content     = {'data': data}
        )

    except NoSuchElementException:
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content     = {'data': []}
        )
    
    except Exception as error:
        print(traceback.print_exc())
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content     = {'detail': f'server error: {error}'}
        )
    
    finally:
        db.close()


@router.get(
    '/{my_study_id}',
    responses = {
        200: {
            "model": GetMyStudiesResponse,
            "description": "마이스터디 조회 성공"
        },
        500: {
            "model": ErrorResponseBase,
            "description": "서버에서 잡지 못한 에러"
        }
    }
)
def get_my_studies(my_study_id: int, db: Session = Depends(get_db)):
    try:
        data = my_studies.get_by_id(db, my_study_id)
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content     = {'data': data}
        )

    except NoSuchElementException:
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content     = {'data': []}
        )
    
    except Exception as error:
        print(traceback.print_exc())
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content     = {'detail': f'server error: {error}'}
        )
    
    finally:
        db.close()
