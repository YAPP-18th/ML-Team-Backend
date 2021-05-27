from app.schemas.responses import SuccessResponseBase


class GetMyStudiesResponse(SuccessResponseBase):
    class Config:
        schema_extra = {
            "example": {
                "data": [
                    {
                        "id": 5,
                        "started_at": "2021-05-25T22:55:16.874569",
                        "ended_at": "2021-05-25T22:59:16.555907",
                        "total_time": 239,
                        "star_count": None,
                        "study_room_id": "7ce741ef-5f97-46ec-9cf6-6eb6b6a4ee9a",
                        "title": "스터디룸 생성 테스트",
                        "disturbances": [
                            {
                                "id": 5,
                                "type": "smartphone",
                                "count": 1,
                                "time": 8
                            },
                            {
                                "id": 9,
                                "type": "sleep",
                                "count": 1,
                                "time": 5
                            }
                        ]
                    },
                    {
                        "id": 6,
                        "started_at": "2021-05-25T23:00:10.040419",
                        "ended_at": "2021-05-25T23:02:49.544101",
                        "total_time": 159,
                        "star_count": None,
                        "study_room_id": "7ce741ef-5f97-46ec-9cf6-6eb6b6a4ee9a",
                        "title": "스터디룸 생성 테스트",
                        "disturbances": [
                            {
                                "id": 6,
                                "type": "await",
                                "count": 1,
                                "time": 20
                            }
                        ]
                    }
                ]
            }
        }