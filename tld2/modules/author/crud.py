from sqlalchemy.ext.asyncio import AsyncSession

from tld2.models import Author


async def create_author(db: AsyncSession, name: str) -> Author:
    db_author = Author(name=name)
    db.add(db_author)
    await db.commit()
    return db_author
