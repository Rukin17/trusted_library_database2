from fastapi import Depends

from sqlalchemy.orm import Session
from fastapi import APIRouter

from tld2 import schemas
from tld2.db import get_db
from tld2.crud import user, approver
from tld2.models import Role


approver_router = APIRouter()


@approver_router.post('/approvers/', response_model=schemas.Approver)
def create_approver(email: str, db: Session = Depends(get_db)):
    db_user = user.get_user_by_email(db=db, email=email)
    new_approver = approver.create_approver(
        db=db,
        fullname=db_user.fullname,
        email=email,
        user_id=db_user.id
    )
    return new_approver


@approver_router.post('/approvers/{approver_id}/ban/', response_model=schemas.Approver)
def ban_approver(id: int, db: Session = Depends(get_db)):
    db_approver = approver.get_approver_by_id(db=db, id=id)
    db_approver.is_active = False
    db.commit()
    return db_approver