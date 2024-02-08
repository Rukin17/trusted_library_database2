from sqlalchemy.orm import Session

from tld2 import models
from tld2.hashing import Hasher
from tld2.models import User


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, username: str, fullname: str, email: str, password: str) -> User:
    hashed_password = Hasher.get_password_hash(password)
    disabled = False
    db_user = models.User(
        username=username,
        fullname=fullname,
        email=email,
        hashed_password=hashed_password,
        disabled=disabled
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user