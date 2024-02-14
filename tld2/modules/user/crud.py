from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tld2.hashing import Hasher
from tld2.models import User


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user_row = result.fetchone()
    if user_row:
        return user_row[0]
    return None


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    user_row = result.fetchone()
    if user_row:
        return user_row[0]
    return None


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user_row = result.fetchone()
    if user_row:
        return user_row[0]
    return None


async def create_user(db: AsyncSession, username: str, fullname: str, email: str, password: str) -> User:
    hashed_password = Hasher.get_password_hash(password)
    disabled = False
    db_user = User(
        username=username,
        fullname=fullname,
        email=email,
        hashed_password=hashed_password,
        disabled=disabled
    )
    db.add(db_user)
    await db.commit()
    return db_user
