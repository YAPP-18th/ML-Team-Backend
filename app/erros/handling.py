from fastapi            import status
from fastapi.exceptions import HTTPException


def get_detail(param: str, field: str, message: str, err: str):
    detail = [
        {
            'loc': [
                f'{param}', # ex. body
                f'{field}'  # ex. title
            ],
            "msg": message, # ex. field required, not found
            "type": f"{err}.missing" # ex. value_error
        }
    ]
    return detail


def not_found_exception_handler(param, field, message, err):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=get_detail(param, field, message, err))


def uncaught_exception_handler():
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='server error')
