import logging
import traceback

import requests
from datetime import datetime, timedelta
from typing import Optional

from fastapi import status, Header
from fastapi.responses import JSONResponse
from jose import jwt, JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError

from app.core import user_settings
from app.errors import get_detail


def parsing_token_decorator(func):
    def wrapper(token: str, **kwargs):
        try:
            return func(token.split(" ")[1], **kwargs)
        except IndexError:
            raise JWTError()

    return wrapper


# DI
def auth_token(authorization: Optional[str] = Header(None)):
    try:
        check_access_token_valid(authorization)
    except JWTError:
        message = traceback.format_exc()
        detail = get_detail(param='token', field='authorize', message=message, err='invalid Google token')
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': detail})


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, user_settings.SECRET_KEY, algorithm=user_settings.ALGORITHM)
    return encoded_jwt


@parsing_token_decorator
def auth_google_token(token: str):
    result = requests.get("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=" + token)

    if result.status_code == 200:
        return result.json()["email"]

    else:
        raise JWTError


@parsing_token_decorator
def check_access_token_valid(token: str, on_board=False):
    try:
        decode_token = jwt.decode(token, user_settings.SECRET_KEY, algorithms=[user_settings.ALGORITHM])
        if on_board:
            return decode_token["on_board"]
        return decode_token["sub"]
    except ExpiredSignatureError as err:
        logging.info("Token has expired")
        # todo: Refresh Token Check
        raise JWTError()
    except JWTClaimsError:
        logging.info("token has any claims")
        raise JWTError()
    except JWTError:
        logging.info("Invalid Signature token")
        raise JWTError()


def check_refresh_token(param):
    # todo : 레디스 연결 이후
    pass
