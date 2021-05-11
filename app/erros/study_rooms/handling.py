from fastapi            import status
from fastapi.exceptions import HTTPException

from app.erros.handling import get_detail


def password_exception_handler():
    detail = get_detail(param='body', field='password', message='field required' ,err='value_error')
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

