from sqlalchemy import Row
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tld2.models import ApprovedLibrary


async def create_approved_library(db: AsyncSession, name: str, approver_id: int, library_id: int) \
        -> ApprovedLibrary:
    db_approved = ApprovedLibrary(name=name, approver_id=approver_id, library_id=library_id)
    db.add(db_approved)
    await db.commit()
    return db_approved


# TODO поправить!
async def get_approved_library(db: AsyncSession, approved_id: int) -> Row[tuple[ApprovedLibrary]] | None:
    query = select(ApprovedLibrary).where(ApprovedLibrary.id == approved_id)
    result = await db.execute(query)
    return result.first()
