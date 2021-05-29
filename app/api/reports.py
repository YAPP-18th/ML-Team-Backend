import traceback

from fastapi                import (
                                APIRouter,
                                Depends,
                                status
                                )
from fastapi.responses      import JSONResponse
from sqlalchemy.orm.session import Session

from app.api.deps           import get_db
from app.crud               import reports
from app.schemas            import (
                                ErrorResponseBase,
                                GetReportReponse,
                                NotFoundReportHandling
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
            "model": GetReportReponse,
            "description": "레포트 조회 성공"
        },
        500: {
            "model": ErrorResponseBase,
            "description": "서버에서 잡지 못한 에러"
        }
    }
)
def get_report(date: str, user_id: str, db: Session=Depends(get_db)):
    try:
        data = reports.get(db, user_id, date)
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content     = {'data': data}
        )

    except NoSuchElementException as element_err:
        message = element_err.message
        detail  = get_detail(param='database', field='report', message=message, err='database')
        return JSONResponse(
            status_code = status.HTTP_404_NOT_FOUND,
            content     = {'detail': detail}
        )

    except Exception as error:
        print(traceback.print_exc())
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content     = {'detail': f'server error: {error}'}
        )
    
    finally:
        db.close()
    
