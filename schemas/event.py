from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from typing import List

from database import get_db
from models.event import Event, Eventer

router = APIRouter(prefix="/events", tags=["events"])


# Pydantic схемы
class EventerResponse(BaseModel):
    id: int
    name: str
    event_id: int
    status: bool
    class Config:
        orm_mode = True


class EventCreate(BaseModel):
    title: str
    dateTimeStart: datetime
    dateTimeEnd: datetime
    placeevent: str
    # comment: str  # Комментарий как строка
    address: str  # Комментарий как строка
    eventers: List[str]  # Список имен участников

class EventerUpdate(BaseModel):
    name: str
    event_id: int
    status: bool
    class Config:
        orm_mode = True

class EventEdit(BaseModel):
    title: str
    placeevent: str
    dateTimeStart: datetime
    dateTimeEnd: datetime
    address: str  # Комментарий как строка
    eventers: List[str] # Список имен участников

class EventResponse(EventCreate):
    id: int
    status: bool
    eventers: List[EventerResponse] = []

    class Config:
        orm_mode = True

class EventDelete(BaseModel):
    id: int