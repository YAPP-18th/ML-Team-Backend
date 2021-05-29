import logging
import traceback
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Header, Response
from fastapi.encoders import jsonable_encoder
from jose import JWTError
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse

from app.crud       import users
from app.api.deps   import get_db
from app.errors      import get_detail, NoSuchElementException
from app.schemas    import (
                            SuccessResponseBase,
                            ErrorResponseBase,
                            UserDataResponse,
                            UserCreate,
                            NotFoundUserHandling,
                            UnauthorizedHandler,
                            ForbiddenHandler
                            )
from app.service    import auth
from app.core       import user_settings

router = APIRouter()


@router.post(
    "/signup",
    responses = {
        200: {
            "model": UserDataResponse,
            "description": "회원가입 성공"
        },
        401: {
            "model": UnauthorizedHandler,
            "description": "JWT 토큰 인증에 실패하였을 경우"
        },
        403: {
            "model": ForbiddenHandler,
            "description": "올바른 유형의 토큰이 아닌 경우(on-board / access)"
        },
        500: {
            "model": ErrorResponseBase,
            "description": "Generic Error"
        }
    }
)
def sign_up(*, db: Session = Depends(get_db),
            user_in: UserCreate,
            authorization: Optional[str] = Header(None)):
    try:
        email = auth.check_access_token_valid(authorization, on_board=True)
        user_in.social_id = email
        user = users.create(db, obj_in=user_in)
        token = auth.create_access_token({"sub": email}, timedelta(minutes=user_settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'data': jsonable_encoder(user)},
                            headers={'Authorization' : 'bearer ' + token})
    except JWTError:
        message = traceback.format_exc()
        detail  = get_detail(param='token', field='authorize', message=message, err='invalid token')
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': detail})
    except NameError:
        message = traceback.format_exc()
        detail = get_detail(param='token', field='forbidden', message=message, err='This token is not on-boarding token')
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': detail})
    except Exception as error:
        logging.error(traceback.format_exc())
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'detail': f'server error: {traceback.format_exc()}'})
    finally:
        db.close()


@router.get(
    "/signin",
    responses = {
        200: {
            "model": UserDataResponse,
            "description": "로그인 성공"
        },
        401: {
            "model": UnauthorizedHandler,
            "description": "Google 토큰 인증에 실패하였을 경우"
        },
        404: {
            "model": NotFoundUserHandling,
            "description": "user가 존재하지 않는 경우"
        },
        500: {
            "model": ErrorResponseBase,
            "description": "Generic Error"
        }
    }
)
def sign_in(*, db: Session = Depends(get_db),
            authorization: Optional[str] = Header(None)
            ):
    try:
        # raise JWT Error
        email = auth.auth_google_token(authorization)
        user = users.get_one_by_email(db, email)

        token = auth.create_access_token({"sub": email}, timedelta(minutes=user_settings.ACCESS_TOKEN_EXPIRE_MINUTES))

        if user is None:
            token = auth.create_access_token({"on_board": email},
                                             timedelta(minutes=user_settings.ACCESS_TOKEN_EXPIRE_MINUTES))
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content={'detail': "user(email: " + email + ") not exist."},
                                headers={"Authorization": 'bearer ' + token}
                                )

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'data': jsonable_encoder(user)},
                            headers={"Authorization": 'bearer ' + token})
    except JWTError:
        message = traceback.format_exc()
        detail = get_detail(param='token', field='authorize', message=message, err='invalid Google token')
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': detail})
    except Exception as error:
        logging.error(traceback.format_exc())
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'detail': f'server error: {traceback.format_exc()}'})
    finally:
        db.close()


@router.get(
    "/get",
    responses = {
        200: {
            "model": UserDataResponse,
            "description": "정상 Response"
        },
        401: {
            "model": UnauthorizedHandler,
            "description": "JWT 토큰 인증에 실패하였을 경우"
        },
        403: {
            "model": ForbiddenHandler,
            "description": "올바른 유형의 토큰이 아닌 경우(on-board / access)"
        },
        404: {
            "model": NotFoundUserHandling,
            "description": "user가 존재하지 않는 경우"
        },
        500: {
            "model": ErrorResponseBase,
            "description": "Generic Error"
        }
    }
)
def get_user(
        *,
        db: Session = Depends(get_db),
        authorization: Optional[str] = Header(None)
):
    try:
        # raise JWT Error
        email = auth.check_access_token_valid(authorization)
        user = users.get_one_by_email(db, email)

        if user is None:
            raise NoSuchElementException("user(email: " + email + ") not exist.")

        return JSONResponse(status_code=status.HTTP_200_OK, content={'data': jsonable_encoder(user)})
    except JWTError:
        message = traceback.format_exc()
        detail = get_detail(param='token', field='authorize', message=message, err='invalid Google token')
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': detail})
    except NameError:
        message = traceback.format_exc()
        detail = get_detail(param='token', field='forbidden', message=message,
                            err='This token is not access token')
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': detail})
    except KeyError:
        message = traceback.format_exc()
        detail = get_detail(param='token', field='forbidden', message=message,
                            err='This token is not access token')
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': detail})
    except Exception as error:
        logging.error(traceback.format_exc())
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'detail': f'server error: {traceback.format_exc()}'})
    finally:
        db.close()


# todo: 서비스 시작 시, 필히 제거!
@router.get('/test/{email}/{token_type}', response_model=SuccessResponseBase, description='토큰 발급 백도어')
def back_door_access(email: str, token_type: str):
    if token_type == 'onboard':
        token = auth.create_access_token({"on_board": email}, timedelta(minutes=user_settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    else:
        token = auth.create_access_token({"sub": email}, timedelta(minutes=user_settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    return JSONResponse(status_code=status.HTTP_200_OK, content={'token': token})
