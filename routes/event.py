import datetime

from fastapi import APIRouter, HTTPException

from schemas.event import EventResponse, EventCreate, EventDelete, EventEdit
from utils import get_current_user
from schemas.user import User
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from models.event import Event, Eventer

router = APIRouter(
    prefix="/api/events",
    tags=['Event']
)


@router.get('/allEvents/{address}')
def get_events(address: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    today = datetime.datetime.now().date()
    start = datetime.datetime.combine(today, datetime.datetime.min.time())
    end = datetime.datetime.combine(today, datetime.datetime.max.time())
    data = db.query(Event).filter(Event.datetime.between(start, end) & (Event.address == address)).all()

    events = [{"id": i.id, "title": i.title, "placeevent": i.placeevent, "address": i.address, "dateTime": i.datetime,
               "comments": i.comment, 'eventers': i.eventers} for i in data]
    return events


@router.get('/myEvents')
def get_events(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    data = db.query(Event).filter(user.email == Event.creater_email).all()

    events = [{"id": i.id, "title": i.title, "status": i.status, "placeevent": i.placeevent, "address": i.address, "dateTimeStart": i.datetime_start, "dateTimeEnd": i.datetime_end, "eventers": i.eventers}
              for i in data]
    return events


@router.get('/event/{id}')
def get_event(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == id).first()
    return {
        "id": event.id,
        "title": event.title,
        "placeevent": event.placeevent,
        "dateTimeStart": event.datetime_start,
        "dateTimeEnd": event.datetime_end,
        "eventers": event.eventers,
        "address": event.address,
    }


@router.put('/event/confirm_event/{eventer_id}')
def edit_eventer(eventer_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    eventer = db.query(Eventer).filter(Eventer.id == eventer_id).first()
    eventer.status = True
    db.commit()
    db.refresh(eventer)
    return {
        "id": eventer.id,
        "name": eventer.name,
        "status": eventer.status,
        'event_id': eventer.event_id
    }


@router.put('/event/{id}')
def update_event(id: int, event_data: EventEdit, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    print(event_data)
    event = db.query(Event).filter(Event.id == id).first()
    event.title = event_data.title
    event.placeevent = event_data.placeevent
    event.datetime_start = event_data.dateTimeStart
    event.datetime_end = event_data.dateTimeEnd
    event.address = event_data.address
    old = [i.name for i in event.eventers]
    new = [i for i in event_data.eventers]
    event.eventers = []

    for i in new:
        eventer = Eventer(name=i)
        event.eventers.append(eventer)
    db.commit()
    db.refresh(event)
    return {
        "id": event.id,
        "title": event.title,
        "placeevent": event.placeevent,
        "dateTimeStart": event.datetime_start,
        "dateTimeEnd": event.datetime_end,
        "status": event.status,
        "eventers": event.eventers,
        "address": event.address,
    }


# Роутер для создания события
@router.post("/create")
def create_event(event_data: EventCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    print(event_data)
    name = user.name
    email = user.email
    try:
        # Создаем основное событие
        db_event = Event(
            title=event_data.title,
            datetime_start=event_data.dateTimeStart,
            datetime_end=event_data.dateTimeEnd,
            creater_name=name,
            creater_email=email,
            address=event_data.address,
            placeevent=event_data.placeevent,
        )
        print(event_data)
        # Добавляем участников
        for eventer_name in event_data.eventers:
            eventer = Eventer(name=eventer_name)
            db_event.eventers.append(eventer)

        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return {
            "id": db_event.id,
            "title": db_event.title,
            "placeevent": db_event.placeevent,
            "dateTimeStart": db_event.datetime_start,
            "dateTimeEnd": db_event.datetime_end,
            "status": db_event.status,
            "eventers": db_event.eventers,
            "address": db_event.address,
        }

    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating event: {str(e)}"
        )


@router.delete('/delete/{event_id}')
def delete_event(event_id: int, db: Session = Depends(get_db),user: User = Depends(get_current_user)):
    try:
        event = db.query(Event).get(event_id)
        print(event)
        db.delete(event)
        db.commit()
        return event.id
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail='Ошибка удаления элемента'
        )


@router.post('/confirm_out/{event_id}')
def confirm_out(event_id: int, db: Session = Depends(get_db),user: User = Depends(get_current_user)):
    try:
        event = db.query(Event).get(event_id)
        print(event)
        print(event.eventers)
        for x in event.eventers:
            x.status = True
        event.status = True
        db.commit()
        return event.eventers[0].status
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail='Ошибка'
        )