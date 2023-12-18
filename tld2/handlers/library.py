from fastapi import Depends, HTTPException
from typing import Annotated

from tld2.auth import get_current_active_user

from sqlalchemy.orm import Session
from fastapi import APIRouter

from tld2 import models, schemas
from tld2.db import get_db
from tld2.crud import library, approver, approved_library


library_router = APIRouter()


@library_router.post('/', response_model=schemas.Library)
def add_library(
    name: str, 
    current_user: Annotated[schemas.User, Depends(get_current_active_user)], 
    db: Session = Depends(get_db)
    ):
    
    new_library = library.create_library(db, name=name)
    
    #TODO  authors

    return new_library


#TODO сделать авторизацию и взять approver_id 
@library_router.post('/{library_id}/approve', response_model=schemas.ApprovedLibrary)
def approve_library(
    library_id: int, 
    approver_id: int, 
    current_user: Annotated[schemas.User, Depends(get_current_active_user)], 
    db: Session = Depends(get_db)
    ):
   
    db_library = library.get_library_by_id(db=db, library_id=library_id)
    if not db_library:
        raise HTTPException(status_code=404, detail=("Library doesn't exists"))
    
    db_approver = approver.get_approver_by_id(db=db, id=approver_id)
    if db_approver.is_active:
        library.change_status(db=db, library=db_library, status=models.Status.APPROVED)
        approve =  approved_library.create_approved_library(
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
    db: Session = Depends(get_db)
    ):

    db_library = library.get_library_by_id(db=db, library_id=library_id)
    if not db_library:
        raise HTTPException(status_code=404, detail=("Library doesn't exists"))
    
    db_approver = approver.get_approver_by_id(db=db, id=approver_id)
    if db_approver.is_active:
        library.change_status(db=db, library=db_library, status=models.Status.MALWARE)
    return db_library

