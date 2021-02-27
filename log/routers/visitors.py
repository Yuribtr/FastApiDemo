from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from log import schemas
from log.database import get_db
from log.repository import visitors
from log.schemas import VisitorOut, VisitorIn
from log.oauth2 import get_current_user

router = APIRouter(
    tags=['Visitors'],
    prefix='/visitors'
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[VisitorOut])
def get_visitors(offset: int = 0, limit: int = 10, db: Session = Depends(get_db),
                 current_user: schemas.UserIn = Depends(get_current_user)):
    return visitors.get_visitors(offset=offset, limit=limit, db=db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=VisitorOut)
def get_visitor_by_id(id: int, db: Session = Depends(get_db),
                      current_user: schemas.UserIn = Depends(get_current_user)):
    return visitors.get_visitor_by_id(id=id, db=db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_visitor(visitor: VisitorIn, db: Session = Depends(get_db),
                   current_user: schemas.UserIn = Depends(get_current_user)):
    return visitors.create_visitor(visitor=visitor, db=db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_visitor_by_id(id: int, visitor: VisitorIn, db: Session = Depends(get_db),
                         current_user: schemas.UserIn = Depends(get_current_user)):
    return visitors.update_visitor_by_id(id=id, visitor=visitor, db=db)


@router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED)
def delete_visitor_by_id(id: int, db: Session = Depends(get_db),
                         current_user: schemas.UserIn = Depends(get_current_user)):
    return visitors.delete_visitor_by_id(id=id, db=db)
