from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Response
from jose import JWTError
from sqlalchemy import null
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api.deps import get_db
from app.schemas import UserResponse
from app.service.user import auth
from app.core import settings

router = APIRouter()


@router.post("/signup", response_model=UserResponse)
def sign_up(*, db: Session = Depends(get_db), user_in: schemas.UserCreate, authorization: Optional[str] = Header(None)):
    if auth.check_access_token_valid(__get_token_in_header(authorization)):
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
        email = auth.auth_google_token(__get_token_in_header(authorization))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")

    user = crud.user.get_one_by_email(db, email)

    if user is None:
        raise HTTPException(status_code=404, detail="user(email: " + email + ") not exist.")

    token = auth.create_access_token({"sub": user.social_id}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    response.headers["Authorization"] = 'bearer ' + token

    return user


def __get_token_in_header(header: str) -> str:
    # bearer gkwlfnbnklvjbopw.wegwedvkls.234352ewfdsv
    return header.split(" ")[1]
