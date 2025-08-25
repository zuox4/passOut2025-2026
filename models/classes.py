from database import Base
from sqlalchemy import Column, String, Integer


class ClassPermission(Base):
    __tablename__ = "classPermission"
    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String(200))
    class_menagers_email = Column(String(200))
