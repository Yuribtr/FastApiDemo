from datetime import datetime
from pydantic.main import BaseModel
from typing import Optional


class VisitorIn(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str]


class VisitorOut(VisitorIn):
    class Config:
        orm_mode = True


class Log(BaseModel):
    visitor: VisitorIn
    visited_at: datetime
    payment: int


class UserIn(BaseModel):
    name: str
    email: str
    password: str


class UserOut(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True
