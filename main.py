from typing import Optional
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"Test": "page"}


@app.get("/about")
def about():
    return {"about": "page"}
