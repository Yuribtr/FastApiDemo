from datetime import datetime
from pydantic.main import BaseModel
from typing import Optional


class VisitorInput(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str]


class VisitorOutput(VisitorInput):
    class Config:
        orm_mode = True


class Log(BaseModel):
    visitor: VisitorInput
    visited_at: datetime
    payment: int
