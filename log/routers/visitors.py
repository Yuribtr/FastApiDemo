from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from log import models
from log.database import get_db
from log.schemas import VisitorOut, VisitorIn

router = APIRouter(
    tags=['Visitors'],
    prefix='/visitors'
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[VisitorOut])
def get_visitors(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    visitors = db.query(models.Visitor).limit(limit).offset(offset).all()
    return visitors


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=VisitorOut)
def get_visitor_by_id(id: int, db: Session = Depends(get_db)):
    visitor = db.query(models.Visitor).filter(models.Visitor.id == id).first()
    if not visitor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Visitor with id "{id}" was not found')
    return visitor


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_visitor(visitor: VisitorIn, db: Session = Depends(get_db)):
    new_visitor = models.Visitor(first_name=visitor.first_name, last_name=visitor.last_name,
                                 middle_name=visitor.middle_name)
    db.add(new_visitor)
    db.commit()
    db.refresh(new_visitor)
    return new_visitor


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_visitor_by_id(id: int, visitor: VisitorIn, db: Session = Depends(get_db)):
    matched_visitor = db.query(models.Visitor).filter(models.Visitor.id == id)
    if not matched_visitor.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Visitor with id "{id}" was not found')
    matched_visitor.update(visitor, synchronize_session=False)
    db.commit()
    return {'detail': f'Visitor with id "{id}" updated'}


@router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED)
def delete_visitor_by_id(id: int, db: Session = Depends(get_db)):
    matched_visitor = db.query(models.Visitor).filter(models.Visitor.id == id)
    if not matched_visitor.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Visitor with id "{id}" was not found')
    matched_visitor.delete(synchronize_session=False)
    db.commit()
    return {'detail': f'Visitor with id "{id}" deleted'}
