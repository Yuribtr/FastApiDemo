from datetime import datetime
from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base


class TimeStamped(Base):
    __abstract__ = True
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.now)


class Visitor(TimeStamped):
    __tablename__ = 'visitors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    middle_name = Column(String(20), nullable=True)
    visits = relationship('Log', secondary='visitors_logs', order_by='desc(Log.visited_at)', lazy='dynamic')


class Log(TimeStamped):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    visited_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    visitors = relationship('Visitor', secondary='visitors_logs', order_by='desc(Visitor.last_name)', lazy='dynamic')


class VisitorLog(TimeStamped):
    __tablename__ = 'visitors_logs'
    __table_args__ = (PrimaryKeyConstraint('log_id', 'visitor_id'),)
    log_id = Column(Integer, ForeignKey('visitors.id'))
    visitor_id = Column(Integer, ForeignKey('logs.id'))
    # can be changed on Money type via "from sqlalchemy.dialects.postgresql import *"
    payment = Column(Integer)
