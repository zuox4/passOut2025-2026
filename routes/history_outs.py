import datetime

from fastapi import APIRouter, HTTPException
from sqlalchemy import func
import find_user
import studentsDB
from schemas.classes import AddPermission
from schemas.event import EventResponse, EventCreate, EventDelete, EventEdit
from schemas.history_outs import CreatePass
from utils import get_current_user
from schemas.user import User
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from models.history_outs import HistoryOuts

router = APIRouter(
    prefix="/api/pass",
    tags=['Passes']
)


@router.post('/createPass')
def create_pass(data: CreatePass, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    print(data)
    newPass = HistoryOuts(
        student_name=data.name,
        teacher_email=user.email,
        datetime=data.dateTime,
        class_name=data.className,
        comments=data.comments,
    )
    db.add(newPass)
    db.commit()
    db.refresh(newPass)
    return {'id': newPass.id, 'name': newPass.student_name, 'email': newPass.teacher_email, 'datetime': newPass.datetime, 'class_name': newPass.class_name, 'comments': newPass.comments}


@router.delete('/{id}')
def create_pass(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    pas = db.query(HistoryOuts).filter(HistoryOuts.id == id).first()
    db.delete(pas)
    db.commit()
    return {'id': id}


@router.get('/userPasses')
def get_my_passes(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    today = datetime.datetime.now().date()
    start = datetime.datetime.combine(today, datetime.datetime.min.time())
    end = datetime.datetime.combine(today, datetime.datetime.max.time())
    passes = db.query(HistoryOuts).filter(
        (HistoryOuts.teacher_email == user.email) & (HistoryOuts.datetime.between(start, end))).all()
    return [{
        'id': pas.id,
        'name': pas.student_name,
        'email': pas.teacher_email,
        "className": pas.class_name,
        "dateTime": pas.datetime
    } for pas in passes]





@router.get('/allPasses/{address}')
def get_today_passes_by_address(address: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    print(address)
    today = datetime.datetime.now().date()
    start = datetime.datetime.combine(today, datetime.datetime.min.time())
    end = datetime.datetime.combine(today, datetime.datetime.max.time())
    addresses = {'Юровская 97': range(1, 4), 'Юровская 99': range(5, 11)}

    passes = db.query(HistoryOuts).filter(HistoryOuts.datetime.between(start, end)).all()
    return [
        {'id': i.id, 'studentName': i.student_name, "dateTime": i.datetime, 'className': i.class_name} for i in passes
        if int(i.class_name.split('-')[0]) in addresses.get(address)
    ]
