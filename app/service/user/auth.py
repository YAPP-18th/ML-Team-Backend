from datetime import datetime, timedelta
from typing import Optional

import requests
from jose import jwt, JWTError

from app.core import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def auth_google_token(token: str):
    return requests.get("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=" + token)


def check_access_token_valid(token: str):
    decode_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return decode_token["expires"] >= datetime.utcnow()


def check_refresh_token(param):
    # todo : 레디스 연결 이후
    pass
