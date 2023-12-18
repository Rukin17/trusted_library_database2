from fastapi import Depends
from typing import Annotated

from tld2.auth import get_current_active_user
from sqlalchemy.orm import Session
from fastapi import APIRouter

from tld2 import schemas
from tld2.db import get_db
from tld2.crud import user, approver
from tld2.crud.role import add_new_role_for_user, get_role_instance_for_user_by_id
from tld2.models import RolesEnum


approver_router = APIRouter()


@approver_router.post('/', response_model=schemas.Approver)
def create_approver(
    email: str,
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
    ):
    
    db_user = user.get_user_by_email(db=db, email=email)
    new_approver = approver.create_approver(
        db=db,
        fullname=db_user.fullname,
        email=email,
        user_id=db_user.id
    )

    db_role_instance = get_role_instance_for_user_by_id(db=db, user_id=db_user.id)
    add_new_role_for_user(db=db, role_instance_from_db=db_role_instance, new_role=RolesEnum.APPROVER)

    return new_approver


@approver_router.post('/{approver_id}/ban/', response_model=schemas.Approver)
def ban_approver(
    id: int, 
    current_user: Annotated[schemas.User, Depends(get_current_active_user)], 
    db: Session = Depends(get_db)
    ):
    db_approver = approver.get_approver_by_id(db=db, id=id)
    db_approver.is_active = False
    db.commit()
    return db_approver