from pydantic import BaseModel
from datetime import datetime


class CreatePass(BaseModel):
    name: str
    dateTime: datetime
    className: str
    comments: str
