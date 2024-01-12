from datetime import timedelta
from typing import Annotated

import sqlalchemy
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from tld2.auth import ACCESS_TOKEN_EXPIRE_MINUTES
from tld2.auth import authenticate_user
from tld2.auth import create_access_token
from tld2.auth import Token
from tld2.db import get_db


login_router = APIRouter()


@login_router.post("/token", response_model=Token)
def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Annotated[sqlalchemy.Engine, Depends(get_db)]):
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
