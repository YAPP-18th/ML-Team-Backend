import logging
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Response
from fastapi.logger import logger
from jose import JWTError
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api.deps import get_db
from app.schemas import UserResponse
from app.service import auth
from app.core import settings
from app.service.auth import get_token_in_header

router = APIRouter()


@router.post("/signup", response_model=UserResponse)
def sign_up(*, db: Session = Depends(get_db), user_in: schemas.UserCreate, authorization: Optional[str] = Header(None)):
    jwt = get_token_in_header(authorization)
    if auth.check_access_token_valid(jwt):
        user = crud.user.create(db, obj_in=user_in)
        return user
    else:
        raise HTTPException(status_code=401, detail='Invalid token')


@router.get("/signin", response_model=UserResponse)
def sign_in(*, db: Session = Depends(get_db),
            response: Response,
            authorization: Optional[str] = Header(None)
            ):
    try:
        email = auth.auth_google_token(get_token_in_header(authorization))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")

    user = crud.user.get_one_by_email(db, email)

    token = auth.create_access_token({"sub": email}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    if user is None:
        raise HTTPException(status_code=404,
                            detail="user(email: " + email + ") not exist.",
                            headers={"Authorization": 'bearer ' + token}
                            )

    response.headers["Authorization"] = 'bearer ' + token

    return user
