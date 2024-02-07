from sqlalchemy.orm import Session

from tld2 import models
from tld2.models import Author


def create_author(db: Session, name: str) -> Author:
    db_author = models.Author(name=name)
    db.add(db_author)
    db.commit()
    return db_author
