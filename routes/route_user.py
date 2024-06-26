from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from sqlalchemy.orm import Session

from core.config import settings
from core.hashed import HashPassword
from core.security import create_access_token
from dbase.datebase import get_db
from schemas.users import UserCreate, UserView
from schemas.token import Token
from dbase.repository.user import (create_new_user, get_user)

router = APIRouter(prefix="/user", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


def authenticate_user(email: str, password: str, db: Session):
    user = get_user(email=email, db=db)
    if not user:
        return False
    if not HashPassword.verify_password(password, user.password):
        return False
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_excrption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="oops"
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_excrption
    except jwt.InvalidTokenError as error:
        raise credentials_excrption from error
    user = get_user(email=email, db=db)
    if user is None:
        raise credentials_excrption
    return user


@router.post("/register", response_model=UserView, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")
