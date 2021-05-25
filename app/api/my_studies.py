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



router = APIRouter()


@router.get()
def get_my_studies():
    pass