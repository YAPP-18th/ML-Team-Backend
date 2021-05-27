from app.schemas.responses import SuccessResponseBase


class GetReportReponse(SuccessResponseBase):
    class Config:
        schema_extra = {
            "example": {
                "data": {
                    "id": 4,
                    "date": "2021-05-25",
                    "achievement": None,
                    "concentration": None,
                    "total_time": 518,
                    "total_star_count": 0,
                    "total_disturbance_counts": 4,
                    "disturbances": [
                        {
                            "type": "smartphone",
                            "total_count": 2,
                            "total_time": 20
                        },
                        {
                            "type": "await",
                            "total_count": 1,
                            "total_time": 20
                        },
                        {
                            "type": "sleep",
                            "total_count": 1,
                            "total_time": 5
                        }
                    ]
                }
            }
        }