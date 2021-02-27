from datetime import datetime
from pydantic.main import BaseModel
from typing import Optional, List


class VisitorIn(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str]


class LogIn(BaseModel):
    visited_at: datetime
    visitor_id: int
    payment: int

    class Config:
        orm_mode = True


class VisitorOut(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str]
    logs: List[LogIn] = []

    class Config:
        orm_mode = True


class LogOut(BaseModel):
    visited_at: datetime
    visitor: VisitorOut
    payment: int

    class Config:
        orm_mode = True


class UserIn(BaseModel):
    name: str
    email: str
    password: str


class UserOut(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True
