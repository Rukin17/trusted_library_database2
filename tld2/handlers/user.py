from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from tld2 import schemas
from tld2.auth import get_current_active_user
from tld2.crud import user
from tld2.crud.role import add_role_for_user
from tld2.crud.role import get_roles
from tld2.db import get_db
from tld2.models import RolesEnum

user_router = APIRouter()


# def get_roles(db: Session = Depends(get_db)):
#     # return list[Role]
#     pass


@user_router.get("/me/", response_model=schemas.User)
def read_users_me(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)]):
    return current_user


@user_router.get("/me/items/")
def read_own_items(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user.username}]


@user_router.post('/', response_model=schemas.User)
def create_user(
        username: str, fullname: str, email: str, password: str,
        db: Session = Depends(get_db)):
    db_user = user.get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')

    new_user = user.create_user(db=db, username=username, fullname=fullname, email=email, password=password)

    user_id = user.get_user_by_email(db=db, email=email).id
    roles = get_roles(db=db, user_id=user_id)
    if RolesEnum.USER in roles:
        raise HTTPException(status_code=403, detail='This role is already in the database')

    add_role_for_user(db=db, user_id=user_id, role=RolesEnum.USER)

    return new_user
