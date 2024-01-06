from sqlalchemy.orm import Session

from tld2.models import Library, Status


def get_library_by_id(db: Session, library_id: int):
    return db.query(Library).filter(Library.id == library_id).first()


def get_libraries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Library).offset(skip).limit(limit).all()


def create_library(db: Session, name: str):
    db_lybrary = Library(name=name, status=Status.UNTESTED)
    db.add(db_lybrary)
    db.commit()
    return db_lybrary


def change_status(db: Session, library: Library, status: Status):
    library.status = status
    db.commit()
    return library
