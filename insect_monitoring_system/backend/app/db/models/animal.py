from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Animal(Base):
    __tablename__ = "animals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
