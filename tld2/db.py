from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from tld2.config import my_config


engine = create_async_engine(my_config.async_db_url, future=True, echo=True,)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_db() -> AsyncGenerator:
    db: AsyncSession = async_session()
    try:
        yield db
    finally:
        await db.close()
