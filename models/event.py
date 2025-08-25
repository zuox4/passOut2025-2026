from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base
from pydantic import BaseModel
from database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    datetime_start = Column(DateTime)
    datetime_end = Column(DateTime)
    creater_name = Column(String(50))
    creater_email = Column(String(50))
    placeevent = Column(String(100))
    status = Column(Boolean, default=False)
    address = Column(String(100))
    eventers = relationship("Eventer", back_populates="event", cascade="all, delete-orphan")


class Eventer(Base):
    __tablename__ = "eventers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    status = Column(Boolean, default=False)
    event_id = Column(Integer, ForeignKey("events.id"))

    event = relationship("Event", back_populates="eventers")
