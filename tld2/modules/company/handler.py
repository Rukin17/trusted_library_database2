from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from tld2 import schemas
from tld2.db import get_db
from tld2.modules.approver.crud import get_approver_by_email
from tld2.modules.auth.auth import get_current_active_user
from tld2.modules.company.crud import create_company

company_router = APIRouter()


@company_router.post('/', response_model=schemas.Company)
async def add_company(
        name: str,
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_db)):
    # if Roles.ADMIN in roles:
    return await create_company(db, name=name)
    # else:
    #     raise HTTPException(status_code=403, detail='')


@company_router.post('/{company_id}/approvers/', response_model=schemas.Approver)
async def bind_approver_to_company(
        email: str,
        company_id: int,
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_db)):
    db_approver = await get_approver_by_email(db, email=email)
    if not db_approver:
        raise HTTPException(status_code=400, detail='Email not registered')
    db_approver.company_id = company_id
    await db.commit()
    return db_approver
