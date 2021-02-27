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
from log.schemas import VisitorIn, VisitorOut, UserIn, UserOut, LogIn, LogOut

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
@app.get('/', response_class=HTMLResponse, tags=['Home'])
async def home_page(request: Request, db: Session = Depends(get_db)):
    message = 'Check out our API'
    visitors = db.query(models.Visitor).all()
    return templates.TemplateResponse('index.html', {'request': request, 'message': message, 'visitors': visitors})


# GET SECTION
@app.get('/visitors', status_code=status.HTTP_200_OK, response_model=List[VisitorOut], tags=['Visitors'])
def get_visitors(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    visitors = db.query(models.Visitor).limit(limit).offset(offset).all()
    return visitors


@app.get('/visitors/{id}', status_code=status.HTTP_200_OK, response_model=VisitorOut, tags=['Visitors'])
def get_visitor_by_id(id: int, db: Session = Depends(get_db)):
    visitor = db.query(models.Visitor).filter(models.Visitor.id == id).first()
    if not visitor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Visitor with id "{id}" was not found')
    return visitor


@app.get('/users/{id}', status_code=status.HTTP_200_OK, response_model=UserOut, tags=['Users'])
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id "{id}" was not found')
    return user


@app.get('/logs', status_code=status.HTTP_200_OK, response_model=List[LogOut], tags=['Logs'])
def get_logs(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logs = db.query(models.Log).limit(limit).offset(offset).all()
    return logs


@app.get('/logs/{id}', status_code=status.HTTP_200_OK, response_model=LogOut, tags=['Users'])
def get_log_by_id(id: int, db: Session = Depends(get_db)):
    log = db.query(models.Log).filter(models.Log.id == id).first()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Log with id "{id}" was not found')
    return log


# CREATE SECTION
@app.post('/visitors', status_code=status.HTTP_201_CREATED, tags=['Visitors'])
def create_visitor(visitor: VisitorIn, db: Session = Depends(get_db)):
    new_visitor = models.Visitor(first_name=visitor.first_name, last_name=visitor.last_name,
                                 middle_name=visitor.middle_name)
    db.add(new_visitor)
    db.commit()
    db.refresh(new_visitor)
    return new_visitor


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserOut, tags=['Users'])
def create_visitor(user: UserIn, db: Session = Depends(get_db)):
    new_user = models.User(name=user.name, email=user.email,
                           password=Hash.bcrypt(pasword=user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post('/logs', status_code=status.HTTP_201_CREATED, tags=['Logs'])
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


# UPDATE SECTION
@app.put('/visitors/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Visitors'])
def update_visitor_by_id(id: int, visitor: VisitorIn, db: Session = Depends(get_db)):
    matched_visitor = db.query(models.Visitor).filter(models.Visitor.id == id)
    if not matched_visitor.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Visitor with id "{id}" was not found')
    matched_visitor.update(visitor, synchronize_session=False)
    db.commit()
    return {'detail': f'Visitor with id "{id}" updated'}


# DELETE SECTION
@app.delete('/visitors/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Visitors'])
def delete_visitor_by_id(id: int, db: Session = Depends(get_db)):
    matched_visitor = db.query(models.Visitor).filter(models.Visitor.id == id)
    if not matched_visitor.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Visitor with id "{id}" was not found')
    matched_visitor.delete(synchronize_session=False)
    db.commit()
    return {'detail': f'Visitor with id "{id}" deleted'}
