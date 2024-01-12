from sqlalchemy.orm import Session

from typing import List
from tld2.models import Role, RolesEnum



# TODO Delete role
12


def add_role_for_user(db: Session, user_id: int, role: RolesEnum) -> Role:
    role_for_user = Role(user_id=user_id, role=role)
    db.add(role_for_user)
    db.commit()
    return role_for_user


def get_roles(db: Session, user_id: int) -> List[Role]:
    return db.query(Role).filter(Role.user_id == user_id).all()


# def get_role_instance_for_user_by_id(db: Session, user_id):
#     return db.query(Role).filter(Role.user_id == user_id).first()


# def add_new_role_for_user(db: Session, role_instance_from_db: Role, new_role: RolesEnum):
#     if new_role == RolesEnum.APPROVER:
#         role_instance_from_db.approver_role = new_role

#     elif new_role == RolesEnum.MANAGER:
#         role_instance_from_db.manager_role = new_role

#     elif new_role == RolesEnum.ADMIN:
#         role_instance_from_db.admin_role = new_role

#     db.commit()
#     return role_instance_from_db
