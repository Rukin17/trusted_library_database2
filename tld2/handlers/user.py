from fastapi import Depends, HTTPException

from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter

from tld2 import schemas
from tld2.db import get_db
from tld2.crud import user
from tld2.crud.role import create_db_role_for_user
from tld2.auth import get_current_active_user
from tld2.models import Role


user_router = APIRouter()


def get_roles(db: Session = Depends(get_db)) -> list[Role]:
    pass


@user_router.get("/me/", response_model=schemas.User)
def read_users_me(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)]
):
    return current_user


@user_router.get("/me/items/")
def read_own_items(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]



@user_router.post('/', response_model=schemas.User)
def create_user(username: str, fullname: str, email: str, password: str, db: Session = Depends(get_db)):
    db_user = user.get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    
    new_user = user.create_user(db=db, username=username, fullname=fullname, email=email, password=password)
    
    user_id = user.get_user_by_email(db=db, email=email).id
    create_db_role_for_user(db=db, user_id=user_id)

    return new_user
    
