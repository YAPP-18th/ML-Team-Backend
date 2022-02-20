from app.schemas.responses import ErrorResponseBase


class NotFoundUserHandling(ErrorResponseBase):
    class Config:
        schema_extra = {
            'example': {
                "detail": [
                    {
                        "loc": [
                            "database",
                            "user"
                        ],
                        "msg": "not found",
                        "type": "database.missing"
                    }
                ]
            }
        }


class UnauthorizedHandler(ErrorResponseBase):
    class Config:
        schema_extra = {
            'example': {
                "detail": [
                    {
                        "loc": [
                            "token",
                            "user"
                        ],
                        "msg": "Unauthorized",
                        "type": "Token Unauthorized"
                    }
                ]
            }
        }


class ForbiddenHandler(ErrorResponseBase):
    class Config:
        schema_extra = {
            'example': {
                "detail": [
                    {
                        "loc": [
                            "token",
                            "user"
                        ],
                        "msg": "Forbidden",
                        "type": "Forbidden Token"
                    }
                ]
            }
        }