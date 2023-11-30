from sqlalchemy.orm import Session

from tld2 import models


def get_library_by_id(db: Session, library_id: int):
    return db.query(models.Library).filter(models.Library.id==library_id).first()


def get_libraries(db: Session, skip : int = 0, limit: int = 100):
    return db.query(models.Library).offset(skip).limit(limit).all()


def create_library(db: Session, name: str):
    db_lybrary = models.Library(name=name, status=models.Status.untested)
    db.add(db_lybrary)
    db.commit()
    return db_lybrary


def change_status(db: Session, library: models.Library, status: models.Status):
    library.status = status
    db.commit()
    return library