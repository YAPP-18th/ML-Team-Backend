from fastapi            import status
from fastapi.exceptions import HTTPException


def get_detail(param: str, field: str, err: str):
    detail = [
        {
            'loc': [
                f'{param}', # ex. body
                f'{field}'  # ex. 
            ],
            "msg": "field required",
            "type": f"{err}.missing" # ex. value_error
        }
    ]
    return detail


def not_found_exception_handler(param, field, err):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=get_detail(param, field, err))


def uncaught_exception_handler():
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='server error')
