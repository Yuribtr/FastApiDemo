from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from log import models
from log.database import engine
from log.routers import users, visitors, logs
from log.database import get_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(users.router)
app.include_router(logs.router)
app.include_router(visitors.router)
models.Base.metadata.create_all(engine)


# SIMPLE START PAGE
@app.get('/', response_class=HTMLResponse, tags=['Home'])
async def home_page(request: Request, db: Session = Depends(get_db)):
    message = 'Check out our API'
    visitors = db.query(models.Visitor).all()
    return templates.TemplateResponse('index.html', {'request': request, 'message': message, 'visitors': visitors})
