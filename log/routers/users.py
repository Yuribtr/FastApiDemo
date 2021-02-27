from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from log import schemas
from log.database import get_db
from log.oauth2 import get_current_user
from log.schemas import UserOut, UserIn
from log.repository import users

router = APIRouter(
    tags=['Users'],
    prefix='/users'
)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db),
                   current_user: schemas.UserIn = Depends(get_current_user)):
    return users.get_user_by_id(id=id, db=db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_visitor(user: UserIn, db: Session = Depends(get_db),
                   current_user: schemas.UserIn = Depends(get_current_user)):
    return users.create_visitor(user=user, db=db)
