from datetime import datetime
from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint, ForeignKey, DateTime
from .database import Base


class TimeStamped(Base):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Visitor(TimeStamped):
    __tablename__ = 'visitors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    middle_name = Column(String(20), nullable=True)


class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    visited_at = Column(DateTime, default=datetime.utcnow)


class GenreMusician(TimeStamped):
    __tablename__ = 'logs_visitors'
    # здесь мы объявляем составной ключ, состоящий из двух полей
    __table_args__ = (PrimaryKeyConstraint('log_id', 'visitor_id'),)
    # В промежуточной таблице явно указываются что следующие поля являются внешними ключами
    log_id = Column(Integer, ForeignKey('visitors.id'))
    visitor_id = Column(Integer, ForeignKey('logs.id'))
    # тип поля может быть заменен на Money через "from sqlalchemy.dialects.postgresql import *"
    payment = Column(Integer)
