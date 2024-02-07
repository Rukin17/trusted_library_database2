from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from sqlalchemy.orm import Session

from tld2 import schemas
from tld2.crud.role import add_role_for_user
from tld2.crud.role import get_roles
from tld2.db import get_db
from tld2.models import RolesEnum
from tld2.modules.user.crud import create_user
from tld2.modules.user.crud import get_user_by_email

user_router = APIRouter()


# def get_roles(db: Session = Depends(get_db)):
#     # return list[Role]
#     pass


@user_router.post('/', response_model=schemas.User)
def create_new_user(
        username: Annotated[str, Form()],
        fullname: Annotated[str, Form()],
        email: Annotated[str, Form()],
        password: Annotated[str, Form()],
        db: Session = Depends(get_db)
):
    db_user = get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')

    new_user = create_user(db=db, username=username, fullname=fullname, email=email, password=password)

    user = get_user_by_email(db=db, email=email)
    if user:
        roles = get_roles(db=db, user_id=user.id)

        if RolesEnum.USER in roles:
            raise HTTPException(status_code=403, detail='This role is already in the database')

        add_role_for_user(db=db, user_id=user.id, role=RolesEnum.USER)

    return new_user
