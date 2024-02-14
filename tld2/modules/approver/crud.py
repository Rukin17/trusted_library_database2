from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tld2 import models
from tld2.models import Approver


async def get_approver_by_email(db: AsyncSession, email: str) -> Approver | None:
    query = select(Approver).where(Approver.email == email)
    result = await db.execute(query)
    approver_row = result.fetchone()
    if approver_row:
        return approver_row[0]
    return None


async def get_approver_by_id(db: AsyncSession, id: int) -> Approver | None:
    query = select(Approver).where(Approver.id == id)
    result = await db.execute(query)
    approver_row = result.fetchone()
    if approver_row:
        return approver_row[0]
    return None


async def get_approvers(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(Approver)
    result = await db.execute(query)
    return result.all()


async def create_approver(db: AsyncSession, fullname: str, email: str, user_id: int) -> Approver:
    db_approver = models.Approver(
        fullname=fullname,
        email=email,
        user_id=user_id
    )
    db.add(db_approver)
    await db.commit()
    return db_approver
