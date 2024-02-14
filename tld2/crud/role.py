from typing import Sequence
from typing import Tuple

from sqlalchemy import Row
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tld2.models import Role
from tld2.models import RolesEnum

# TODO Delete role


async def add_role_for_user(db: AsyncSession, user_id: int, role: RolesEnum) -> Role:
    role_for_user = Role(user_id=user_id, role=role)
    db.add(role_for_user)
    await db.commit()
    return role_for_user


async def get_roles(db: AsyncSession, user_id: int) -> Sequence[Row[Tuple[Role]]]:   # TODO -> list[Role]
    query = select(Role).where(Role.user_id == user_id)
    result = await db.execute(query)
    return result.all()
