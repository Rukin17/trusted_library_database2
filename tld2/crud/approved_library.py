from sqlalchemy.orm import Session

from tld2 import models
from tld2.models import ApprovedLibrary


def create_approved_library(db: Session, name: str, approver_id: int, library_id: int) \
        -> ApprovedLibrary:
    db_approved = models.ApprovedLibrary(name=name, approver_id=approver_id, library_id=library_id)
    db.add(db_approved)
    db.commit()
    return db_approved


def get_approved_library(db: Session, approved_id: int) -> ApprovedLibrary | None:
    return db.query(models.ApprovedLibrary).filter(models.ApprovedLibrary.id == approved_id).first()
