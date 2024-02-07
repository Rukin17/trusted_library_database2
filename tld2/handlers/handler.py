from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from tld2 import schemas
from tld2.crud.role import add_role_for_user
from tld2.crud.role import get_roles
from tld2.db import get_db
from tld2.models import RolesEnum
from tld2.modules.approver.crud import create_approver
from tld2.modules.approver.crud import get_approver_by_id
from tld2.modules.auth.auth import get_current_active_user
from tld2.modules.user.crud import get_user_by_email


approver_router = APIRouter()


@approver_router.post('/', response_model=schemas.Approver)
def add_approver(
        email: str,
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)):
    db_user = get_user_by_email(db=db, email=email)
    if db_user:
        new_approver = create_approver(
            db=db,
            fullname=db_user.fullname,
            email=email,
            user_id=db_user.id
        )

        roles = get_roles(db=db, user_id=db_user.id)
        if RolesEnum.APPROVER in roles:
            raise HTTPException(status_code=403, detail='This role is already in the database')
        add_role_for_user(db=db, user_id=db_user.id, role=RolesEnum.APPROVER)

    return new_approver


@approver_router.post('/{approver_id}/ban/', response_model=schemas.Approver)
def ban_approver(
        id: int,
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)):
    db_approver = get_approver_by_id(db=db, id=id)
    if db_approver:
        db_approver.is_active = False
        db.commit()
        return db_approver
