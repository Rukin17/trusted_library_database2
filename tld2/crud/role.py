from sqlalchemy.orm import Session

from tld2.models import Role, RolesEnum


def create_db_role_for_user(db: Session, user_id: int):
    db_role_for_user = Role(user_id=user_id)
    db.add(db_role_for_user)
    db.commit()
    return db_role_for_user


def get_role_instance_for_user_by_id(db: Session, user_id):
    return db.query(Role).filter(Role.user_id == user_id).first()


def add_new_role_for_user(db: Session, role_instance_from_db: Role, new_role: RolesEnum):
    if new_role == RolesEnum.APPROVER:
        role_instance_from_db.approver_role = RolesEnum.APPROVER

    elif new_role == RolesEnum.MANAGER:
        role_instance_from_db.manager_role = RolesEnum.MANAGER

    elif new_role == RolesEnum.ADMIN:
        role_instance_from_db.admin_role = RolesEnum.ADMIN

    db.commit()
    return role_instance_from_db


#TODO Delete role