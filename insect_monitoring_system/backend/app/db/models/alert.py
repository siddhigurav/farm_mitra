from sqlalchemy import Column, Integer, String, DateTime
from app.db.base import Base
import datetime

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(255), index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
