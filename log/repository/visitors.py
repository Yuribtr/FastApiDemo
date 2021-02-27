from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status
from log import models
from log.schemas import VisitorIn


def get_visitors(offset: int = 0, limit: int = 10, db: Session = None):
    visitors = db.query(models.Visitor).limit(limit).offset(offset).all()
    return visitors


def get_visitor_by_id(id: int, db: Session):
    visitor = db.query(models.Visitor).filter(models.Visitor.id == id).first()
    if not visitor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Visitor with id "{id}" was not found')
    return visitor


def create_visitor(visitor: VisitorIn, db: Session):
    new_visitor = models.Visitor(first_name=visitor.first_name, last_name=visitor.last_name,
                                 middle_name=visitor.middle_name)
    db.add(new_visitor)
    db.commit()
    db.refresh(new_visitor)
    return new_visitor


def update_visitor_by_id(id: int, visitor: VisitorIn, db: Session):
    matched_visitor = db.query(models.Visitor).filter(models.Visitor.id == id)
    if not matched_visitor.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Visitor with id "{id}" was not found')
    matched_visitor.update(visitor, synchronize_session=False)
    db.commit()
    return {'detail': f'Visitor with id "{id}" updated'}


def delete_visitor_by_id(id: int, db: Session):
    matched_visitor = db.query(models.Visitor).filter(models.Visitor.id == id)
    if not matched_visitor.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Visitor with id "{id}" was not found')
    matched_visitor.delete(synchronize_session=False)
    db.commit()
    return {'detail': f'Visitor with id "{id}" deleted'}
