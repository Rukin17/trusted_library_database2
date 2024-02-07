from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from tld2 import models
from tld2 import schemas
from tld2.crud.approved_library import create_approved_library
from tld2.db import get_db
from tld2.modules.approver.crud import get_approver_by_id
from tld2.modules.auth.auth import get_current_active_user
from tld2.modules.library.crud import change_status
from tld2.modules.library.crud import create_library
from tld2.modules.library.crud import get_library_by_id

library_router = APIRouter()


@library_router.post('/', response_model=schemas.Library)
def add_library(
        name: str,
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)):
    new_library = create_library(db, name=name)
    # TODO  authors

    return new_library


# TODO сделать авторизацию и взять approver_id
@library_router.post('/{library_id}/approve', response_model=schemas.ApprovedLibrary)
def approve_library(
        library_id: int,
        approver_id: int,
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)):
    db_library = get_library_by_id(db=db, library_id=library_id)
    if not db_library:
        raise HTTPException(status_code=404, detail=("Library doesn't exists"))

    db_approver = get_approver_by_id(db=db, id=approver_id)
    if db_approver and db_approver.is_active:
        change_status(db=db, library=db_library, status=models.Status.APPROVED)
        # TODO Бага: если библиотека аппрувнута, потом бан, потом снова аппрув и пытается добавить в аппрув либрари
        approve = create_approved_library(
            db=db,
            name=db_library.name,
            approver_id=approver_id,
            library_id=library_id
        )
        return approve


@library_router.post('/{library_id}/ban', response_model=schemas.Library)
def ban_library(
        library_id: int, approver_id: int,
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)):
    db_library = get_library_by_id(db=db, library_id=library_id)
    if not db_library:
        raise HTTPException(status_code=404, detail=("Library doesn't exists"))

    db_approver = get_approver_by_id(db=db, id=approver_id)
    if db_approver and db_approver.is_active:
        change_status(db=db, library=db_library, status=models.Status.MALWARE)
    return db_library
