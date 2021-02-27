from datetime import datetime
from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base


class TimeStamped(Base):
    __abstract__ = True
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class Visitor(TimeStamped):
    __tablename__ = 'visitors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    middle_name = Column(String(50), nullable=True)
    logs = relationship('Log', back_populates='visitor')


class Log(TimeStamped):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    visited_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    # can be changed on Money type via "from sqlalchemy.dialects.postgresql import *"
    payment = Column(Integer)
    visitor_id = Column(Integer, ForeignKey('visitors.id'))
    visitor = relationship('Visitor', back_populates='logs')


class User(TimeStamped):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(50), unique=True)
    # https://security.stackexchange.com/a/39851
    password = Column(String(72))
