from typing   import Union

from pydantic import BaseModel


class SuccessResponseBase(BaseModel):
    data: Union[list, dict, None]

    class Config:
        schema_extra = {
            'example': {
                'data': ''
            }
        }


class ErrorResponseBase(BaseModel):
    detail: Union[dict, str]

    class Config:
        schema_extra = {
            'example': {
                'detail': 'server error'
            }
        }


class MethodNotAllowedHandling(ErrorResponseBase):
    class Config:
        schema_extra = {
            "example": {
                "detail": "Method Not Allowed"
            }
        }