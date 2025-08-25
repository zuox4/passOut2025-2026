from pydantic import BaseModel


class Address(BaseModel):
    data: str
