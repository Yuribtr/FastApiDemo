from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from log import models
from log.database import get_db
from log.hashing import Hash
from log.schemas import UserOut, UserIn

router = APIRouter(
    tags=['Users'],
    prefix='/users'
)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id "{id}" was not found')
    return user


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_visitor(user: UserIn, db: Session = Depends(get_db)):
    new_user = models.User(name=user.name, email=user.email,
                           password=Hash.bcrypt(pasword=user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
