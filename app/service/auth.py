from datetime import datetime, timedelta
from typing import Optional

import requests
from fastapi import HTTPException
from jose import jwt, JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError

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
    result = requests.get("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=" + token)

    if result.status_code == 200:
        return result.json()["email"]

    else:
        raise JWTError


def check_access_token_valid(token: str):
    try:
        decode_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return True

    except ExpiredSignatureError:
        print("time")
        return False
    except JWTClaimsError:
        print("claim")
        return False
    except JWTError:
        print("jwt")
        return False


def get_token_in_header(header: str) -> str:
    # bearer gkwlfnbnklvjbopw.wegwedvkls.234352ewfdsv
    return header.split(" ")[1]


def check_refresh_token(param):
    # todo : 레디스 연결 이후
    pass
