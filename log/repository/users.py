from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from log import models
from log.database import get_db
from log.hashing import Hash
from log.schemas import UserIn


def get_user_by_id(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id "{id}" was not found')
    return user


def create_user(user: UserIn, db: Session = Depends(get_db)):
    new_user = models.User(name=user.name, email=user.email,
                           password=Hash.bcrypt(pasword=user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
