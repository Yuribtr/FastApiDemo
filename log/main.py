from fastapi import FastAPI, Depends
from sqlalchemy.dialects.postgresql import psycopg2
from sqlalchemy.orm import Session
from log import models
from log.database import engine, SessionLocal
from log.schemas import Visitor

app = FastAPI()

# make migrations
models.Base.metadata.create_all(engine)


# dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/logs')
def get_logs(limit: int = 10):
    return {'data': 'not implemented'}


@app.get('/logs/{id}')
def get_logs_by_id(id: int):
    return {'data': 'not implemented'}


@app.get('/visitor/{id}')
def get_visitors_by_id(id: int, limit=10):
    return {'data': 'not implemented'}


# CREATE SECTION
@app.post('/visitors')
def create_visitor(visitor: Visitor, db: Session = Depends(get_db)):
    new_visitor = models.Visitor(first_name=visitor.first_name, last_name=visitor.last_name,
                                 middle_name=visitor.middle_name)
    db.add(new_visitor)
    db.commit()
    db.refresh(new_visitor)
    return new_visitor
