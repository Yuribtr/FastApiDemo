from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from log import models
from log.database import get_db
from log.schemas import LogOut, LogIn

router = APIRouter(
    tags=['Logs'],
    prefix='/logs'
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[LogOut])
def get_logs(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logs = db.query(models.Log).limit(limit).offset(offset).all()
    return logs


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=LogOut)
def get_log_by_id(id: int, db: Session = Depends(get_db)):
    log = db.query(models.Log).filter(models.Log.id == id).first()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Log with id "{id}" was not found')
    return log


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_log(log: LogIn, db: Session = Depends(get_db)):
    visitor = db.query(models.Visitor).filter(models.Visitor.id == log.visitor_id).first()
    if not visitor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Visitor with id "{log.visitor_id}" was not found')
    new_log = models.Log(visited_at=log.visited_at, payment=log.payment, visitor_id=log.visitor_id)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log
