from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from typing import Annotated
from typing import Literal

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from tld2 import schemas
from tld2.config import my_config
from tld2.db import get_db
from tld2.hashing import Hasher
from tld2.modules.user.crud import get_user_by_username
from tld2.schemas import User

ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login/token')


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


@dataclass
class UserInDB:
    id: int
    username: str
    fullname: str
    email: str
    hashed_password: str
    disabled: bool


async def get_user(db: AsyncSession, username: str) -> UserInDB:
    db_user = await get_user_by_username(db, username=username)
    if db_user:
        user_in_db = UserInDB(
            db_user.id,
            db_user.username,
            db_user.fullname,
            db_user.email,
            db_user.hashed_password,
            db_user.disabled,
        )
    return user_in_db


async def authenticate_user(db: AsyncSession, username: str, password: str) -> UserInDB | Literal[False]:
    user = await get_user(db, username=username)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


async def create_access_token(data: dict[str, str | datetime], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, my_config.secret_key, algorithm=my_config.algorithm)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)) \
        -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, my_config.secret_key, algorithms=[my_config.algorithm])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[schemas.User, Depends(get_current_user)]) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
