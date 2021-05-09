from typing import Union

from pydantic import BaseModel

class Response(BaseModel):
    data: Union[list, dict, None]

    class Config:
        schema_extra = {
            'example': {
                'data': ''
            }
        }