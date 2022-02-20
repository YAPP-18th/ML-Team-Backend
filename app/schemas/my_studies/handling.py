from app.schemas.responses import ErrorResponseBase


class NotFoundMyStudiesHandling(ErrorResponseBase):
    class Config:
        schema_extra = {
            'example': {
                "detail": [
                    {
                        "loc": [
                            "database",
                            "my studies"
                        ],
                        "msg": "not found",
                        "type": "database.missing"
                    }
                ]
            }
        }
