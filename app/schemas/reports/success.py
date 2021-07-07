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
                    "statuses": [
                        {
                            "name": "smartphone",
                            "value": 2,
                            "total_time": 20
                        },
                        {
                            "name": "await",
                            "value": 1,
                            "total_time": 20
                        },
                        {
                            "name": "sleep",
                            "value": 1,
                            "total_time": 5
                        }
                    ],
                    "max_status": [
                        "smartphone"
                    ]
                }
            }
        }