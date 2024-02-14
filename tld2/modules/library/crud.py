from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tld2.models import Library
from tld2.models import Status


async def get_library_by_id(db: AsyncSession, library_id: int) -> Library | None:
    query = select(Library).where(Library.id == library_id)
    result = await db.execute(query)
    library_row = result.fetchone()
    if library_row:
        return library_row[0]
    return None


async def get_libraries(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(Library)
    result = await db.execute(query)
    return result.all()


async def create_new_library(db: AsyncSession, name: str) -> Library:
    db_lybrary = Library(name=name, status=Status.UNTESTED)
    db.add(db_lybrary)
    await db.commit()
    return db_lybrary


async def change_status(db: AsyncSession, library: Library, status: Status) -> Library:
    library.status = status
    await db.commit()
    return library
