from datetime import timedelta
from typing import Dict

from fastapi.testclient import TestClient
from jose import jwt, JWTError

from app.core import settings
from app.service.user.auth import create_access_token, auth_google_token, check_access_token_valid


def test_create_token() -> None:
    # 토큰의 생성이 이루어지는 지 테스트
    # payload 테스트
    data = {"body": "test"}
    access_token_expires = timedelta(minutes=15)
    token = create_access_token(data, access_token_expires)
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    actual = payload.get("body")

    assert actual == "test"


def test_auth_google_token() -> None:
    # 잘못된 토큰에 대하여 status 400 반환
    wrong_token = "test"
    actual = auth_google_token(wrong_token).status_code

    assert actual == 400


def test_check_access_token_valid() -> None:
    test_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZXN0IjoidGVzdCIsImV4cCI6MTYyMDMwNjQzMH0' \
                 '.1c4BevvQ3IvPJSPBYQGMfwArVNpxOwO_qUhGwycYAuc '
    actual = check_access_token_valid(test_token)

    assert actual is False


# def test_check_refresh_token() -> None:
#     # redis의 ref 토큰을 확인.
#     user_id = 15
#     actual = check_refresh_token(15)
#
#     assert actual is not None
