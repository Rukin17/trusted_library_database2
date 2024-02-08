from sqlalchemy.orm import Session

from tld2.models import Role
from tld2.models import RolesEnum

# TODO Delete role


def add_role_for_user(db: Session, user_id: int, role: RolesEnum) -> Role:
    role_for_user = Role(user_id=user_id, role=role)
    db.add(role_for_user)
    db.commit()
    return role_for_user


def get_roles(db: Session, user_id: int) -> list[Role]:
    return db.query(Role).filter(Role.user_id == user_id).all()
