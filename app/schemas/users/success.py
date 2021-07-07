from app.schemas import SuccessResponseBase


class UserDataResponse(SuccessResponseBase):
    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'provider': 'google',
                'social_id': 'example@gmail.com',
                'nickname': 'new Nickname',
                'goal': {
                    'MON': 2,
                    'TUE': 2,
                    'WED': 2,
                    'THU': 2,
                    'FRI': 2,
                    'SAT': 2,
                    'SUN': 2
                }
            }
        }