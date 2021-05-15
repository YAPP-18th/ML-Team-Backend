import logging
import traceback
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Header, Response
from jose import JWTError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from app import schemas, crud
from app.api.deps import get_db
from app.erros import get_detail, NoSuchElementException
from app.schemas import SuccessResponseBase, ErrorResponseBase, NotFoundUserHandling, UnauthorizedHandler
from app.service import auth
from app.core import user_settings

router = APIRouter()


@router.post(
    "/signup",
    responses = {
        200: {
            "model": SuccessResponseBase,
            "description": "회원가입 성공"
        },
        401: {
            "model": UnauthorizedHandler,
            "description": "JWT 토큰 인증에 실패하였을 경우"
        },
        500: {
            "model": ErrorResponseBase,
            "description": "Generic Error"
        }
    }
)
def sign_up(*, db: Session = Depends(get_db), user_in: schemas.UserCreate, authorization: Optional[str] = Header(None)):
    try:
        email = auth.check_access_token_valid(authorization)
        user_in.social_id = email
        user = crud.user.create(db, obj_in=user_in)
        return JSONResponse(status_code=status.HTTP_200_OK, content={'data': user})
    except JWTError:
        message = traceback.format_exc()
        detail  = get_detail(param='token', field='authorize', message=message, err='invalid token')
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': detail})
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
            "model": SuccessResponseBase,
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
            response: Response,
            authorization: Optional[str] = Header(None)
            ):
    try:
        # raise JWT Error
        email = auth.auth_google_token(authorization)
        user = crud.user.get_one_by_email(db, email)

        token = auth.create_access_token({"sub": email}, timedelta(minutes=user_settings.ACCESS_TOKEN_EXPIRE_MINUTES))

        if user is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content={'detail': "user(email: " + email + ") not exist."},
                                headers={"Authorization": 'bearer ' + token}
                                )

        response.headers["Authorization"] = 'bearer ' + token

        return JSONResponse(status_code=status.HTTP_200_OK, content={'data': user})
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
