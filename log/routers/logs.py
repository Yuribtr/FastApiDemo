from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from log import models
from log.database import get_db
from log.repository import logs
from log.schemas import LogOut, LogIn

router = APIRouter(
    tags=['Logs'],
    prefix='/logs'
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[LogOut])
def get_logs(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return logs.get_logs(offset=offset, limit=limit, db=db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=LogOut)
def get_log_by_id(id: int, db: Session = Depends(get_db)):
    return logs.get_log_by_id(id=id, db=db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_log(log: LogIn, db: Session = Depends(get_db)):
    return logs.create_log(log=log, db=db)
