from datetime import datetime
from pydantic.main import BaseModel
from typing import Optional


class Visitor(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str]


class Log(BaseModel):
    visitor: Visitor
    visited_at: datetime
    payment: int
