from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base
from pydantic import BaseModel
from database import Base


class HistoryOuts(Base):
    __tablename__ = 'history_outs'
    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String(200))
    teacher_email = Column(String(200))
    datetime = Column(DateTime)
    class_name = Column(String(200))
    comments = Column(String(200))
