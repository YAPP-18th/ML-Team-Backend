from app.schemas.responses import ErrorResponseBase


class NotFoundStudyRoomHandling(ErrorResponseBase):
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


class PasswordNeedyStudyRoomHandling(ErrorResponseBase):
    class Config:
        schema_extra = {
            'example': {
                "detail": [
                    {
                        "loc": [
                            "body",
                            "password"
                        ],
                        "msg": "field required",
                        "type": "value_error.missing"
                    }
                ] 
            }
        }


class BodyNeedyStudyRoomHandling(ErrorResponseBase):
    class Config:
         schema_extra = {
            'example': {
                "detail": [
                    {
                        "loc": [
                            "body",
                            "title"
                        ],
                        "msg": "field required",
                        "type": "value_error.missing"
                    },
                    {
                        "loc": [
                            "body",
                            "description"
                        ],
                        "msg": "field required",
                        "type": "value_error.missing"
                    }
                ]
            }
        }       


class QueryNeedyStudyRoomHandling(ErrorResponseBase):
    class Config:
        schema_extra = {
            'example': {
                "detail": [
                    {
                        "loc": [
                            "query",
                            "skip"
                        ],
                        "msg": "field required",
                        "type": "value_error.missing"
                    },
                    {
                        "loc": [
                            "query",
                            "limit"
                        ],
                        "msg": "field required",
                        "type": "value_error.missing"
                    }
                ]
            }
        }


class NoEmptyRoomHandling(ErrorResponseBase):
    class Config:
        schema_extra = {
            'example': {
                "detail": [
                    {
                        "loc": [
                            "database",
                            "study room"
                        ],
                        "msg": "no empty",
                        "type": "database"
                    }
                ]
            }
        }    


class ForbiddenPasswordHandling(ErrorResponseBase):
    class Config:
        schema_extra = {
            'example': {
                "detail": [
                    {
                        "loc": [
                            "body",
                            "password"
                        ],
                        "msg": "forbidden",
                        "type": "invalid"
                    }
                ]
            }
        }   


class ForbiddenUserHandling(ErrorResponseBase):
    class Config:
        schema_extra = {
            'example': {
                "detail": [
                    {
                        "loc": [
                            "database",
                            "user"
                        ],
                        "msg": "forbidden",
                        "type": "invalid"
                    }
                ]
            }
        }

class AlreadyJoinedHandling(ErrorResponseBase):
    class Config:
        schema_extra = {
            'example': {
                "detail": [
                    {
                        "loc": [
                            "database",
                            "user"
                        ],
                        "msg": "Already Connect a Study-Room",
                        "type": "invalid"
                    }
                ]
            }
        }                      