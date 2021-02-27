from typing import List
from fastapi import FastAPI, Depends, Response, HTTPException
from sqlalchemy.dialects.postgresql import psycopg2
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from log import models
from log.database import engine, SessionLocal
from log.hashing import Hash
from log.schemas import VisitorIn, VisitorOut, UserIn, UserOut


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# make migrations
models.Base.metadata.create_all(engine)


# dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# SIMPLE START PAGE
@app.get('/', response_class=HTMLResponse)
async def home_page(request: Request, db: Session = Depends(get_db)):
    message = 'Check out our API'
    visitors = db.query(models.Visitor).all()
    return templates.TemplateResponse('index.html', {'request': request, 'message': message, 'visitors': visitors})


# GET SECTION
@app.get('/visitors', status_code=status.HTTP_200_OK, response_model=List[VisitorOut])
def get_visitors(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    visitors = db.query(models.Visitor).limit(limit).offset(offset).all()
    return visitors


@app.get('/visitors/{id}', status_code=status.HTTP_200_OK, response_model=VisitorOut)
def get_visitor_by_id(id: int, db: Session = Depends(get_db)):
    visitor = db.query(models.Visitor).filter(models.Visitor.id == id).first()
    if not visitor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Visitor with id "{id}" was not found')
    return visitor


@app.get('/users/{id}', status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id "{id}" was not found')
    return user


# CREATE SECTION
@app.post('/visitors', status_code=status.HTTP_201_CREATED)
def create_visitor(visitor: VisitorIn, db: Session = Depends(get_db)):
    new_visitor = models.Visitor(first_name=visitor.first_name, last_name=visitor.last_name,
                                 middle_name=visitor.middle_name)
    db.add(new_visitor)
    db.commit()
    db.refresh(new_visitor)
    return new_visitor


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_visitor(user: UserIn, db: Session = Depends(get_db)):
    new_user = models.User(name=user.name, email=user.email,
                           password=Hash.bcrypt(pasword=user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# UPDATE SECTION
@app.put('/visitors/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_visitor_by_id(id: int, visitor: VisitorIn, db: Session = Depends(get_db)):
    matched_visitor = db.query(models.Visitor).filter(models.Visitor.id == id)
    if not matched_visitor.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Visitor with id "{id}" was not found')
    matched_visitor.update(visitor, synchronize_session=False)
    db.commit()
    return {'detail': f'Visitor with id "{id}" updated'}


# DELETE SECTION
@app.delete('/visitors/{id}', status_code=status.HTTP_202_ACCEPTED)
def delete_visitor_by_id(id: int, db: Session = Depends(get_db)):
    matched_visitor = db.query(models.Visitor).filter(models.Visitor.id == id)
    if not matched_visitor.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Visitor with id "{id}" was not found')
    matched_visitor.delete(synchronize_session=False)
    db.commit()
    return {'detail': f'Visitor with id "{id}" deleted'}
