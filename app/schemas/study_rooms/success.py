from app.schemas.responses import SuccessResponseBase


class GetStudyRoomResponse(SuccessResponseBase):
    class Config:
        schema_extra = {
            'example': {
                'data': {
                    "is_public": False,
                    "style": "style_1",
                    "title": "스터디 룸 제목 수정",
                    "created_at": "2021-05-09T20:50:11.782727",
                    "id": "3d37627c-d87d-469e-8bf3-db7e796838cf",
                    "description": "스터디룸 설명",
                    "current_join_counts": 1,
                    "owner_id": 1
                }
            }
        }


class GetStudyRoomsResponse(SuccessResponseBase):
    class Config:
        schema_extra = {
            'example': {
                'data': [
                    {
                        "title": "스터디 룸 제목 수정",
                        "style": "style_2",
                        "is_public": False,
                        "created_at": "2021-05-09T20:50:11.782727",
                        "description": "스터디룸 설명",
                        "id": "3d37627c-d87d-469e-8bf3-db7e796838cf",
                        "current_join_counts": 1,
                        "owner_id": 1
                    },
                    {
                        "title": "스터디룸 생성 제목",
                        "style": "style_2",
                        "is_public": True,
                        "created_at": "2021-05-09T20:50:11.782727",
                        "description": "스터디룸 설명",
                        "id": "3b199025-92d7-4214-8f9c-b8224d81fca5",
                        "current_join_counts": 3,
                        "owner_id": 1
                    }
                ]
            }
        }