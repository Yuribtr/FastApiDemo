from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from log import schemas
from log.database import get_db
from log.oauth2 import get_current_user
from log.schemas import UserOut, UserIn
from log.repository import users
import re

router = APIRouter(
    tags=['Users'],
    prefix='/users'
)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db),
                   current_user: schemas.UserIn = Depends(get_current_user)):
    return users.get_user_by_id(id=id, db=db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserIn, db: Session = Depends(get_db),
                current_user: schemas.UserIn = Depends(get_current_user)):
    if not re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", user.email):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f'Provided email {user.email} is incorrect')
    return users.create_user(user=user, db=db)
