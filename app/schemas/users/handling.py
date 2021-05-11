from app.schemas.responses import ErrorResponseBase


class NotFoundUserHandling(ErrorResponseBase):
    class Config:
        schema_extra = {
            'example': {
                "detail": [
                    {
                        "loc": [
                            "database",
                            "study room"
                        ],
                        "msg": "not found",
                        "type": "database.missing"
                    }
                ]
            }
        }