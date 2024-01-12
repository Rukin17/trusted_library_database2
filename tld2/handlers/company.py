from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from tld2 import schemas
from tld2.auth import get_current_active_user
from tld2.crud import approver
from tld2.crud import company
from tld2.db import get_db


company_router = APIRouter()


@company_router.post('/', response_model=schemas.Company)
def create_company(
        name: str,
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)):
    # if Roles.ADMIN in roles:
    return company.create_company(db, name=name)
    # else:
    #     raise HTTPException(status_code=403, detail='')


@company_router.post('/{company_id}/approvers/', response_model=schemas.Approver)
def bind_approver_to_company(
        email: str,
        company_id: int,
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)):
    db_approver = approver.get_approver_by_email(db, email=email)
    if not db_approver:
        raise HTTPException(status_code=400, detail='Email not registered')
    db_approver.company_id = company_id
    db.commit()
    return db_approver
