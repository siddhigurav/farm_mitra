from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True, index=True)
    recommendation = Column(String(255))
