from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tld2.models import Company


async def create_company(db: AsyncSession, name: str) -> Company:
    db_company = Company(name=name)
    db.add(db_company)
    await db.commit()
    return db_company


async def get_company_by_id(db: AsyncSession, id: int) -> Company | None:
    query = select(Company).where(Company.id == id)
    result = await db.execute(query)
    company_row = result.fetchone()
    if company_row:
        return company_row[0]
    return None
