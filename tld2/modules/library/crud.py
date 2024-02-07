from sqlalchemy.orm import Session

from tld2.models import Library
from tld2.models import Status


def get_library_by_id(db: Session, library_id: int) -> Library | None:
    return db.query(Library).filter(Library.id == library_id).first()


def get_libraries(db: Session, skip: int = 0, limit: int = 100) -> list[Library]:
    return db.query(Library).offset(skip).limit(limit).all()


def create_library(db: Session, name: str) -> Library:
    db_lybrary = Library(name=name, status=Status.UNTESTED)
    db.add(db_lybrary)
    db.commit()
    return db_lybrary


def change_status(db: Session, library: Library, status: Status) -> Library:
    library.status = status
    db.commit()
    return library
