from app.schemas.responses import ErrorResponseBase


class NotFoundReportHandling(ErrorResponseBase):
    class Config:
        schema_extra = {
            'example': {
                "detail": [
                    {
                        "loc": [
                            "database",
                            "report"
                        ],
                        "msg": "not found",
                        "type": "database.missing"
                    }
                ]
            }
        }
