from sqlalchemy import create_engine
from app.db.base import Base
from app.db.models.user import User
from app.db.models.crop import Crop
from app.db.models.insect import Insect
from app.db.models.remedy import RemedyApproval
from app.db.models.weather import Weather
from app.db.session import engine
from app.core.config import settings
import hashlib

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a default user for testing
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    # Check if default user exists
    existing_user = db.query(User).filter(User.username == "Siddhi").first()
    if not existing_user:
        # Create a default user with a hashed password
        hashed_password = hashlib.sha256("password123".encode()).hexdigest()
        default_user = User(
            username="Siddhi",
            email="siddhi@example.com",
            hashed_password=hashed_password
        )
        db.add(default_user)
        db.commit()
        print("Default user 'Siddhi' created successfully")
    else:
        print("Default user 'Siddhi' already exists")
    
    db.close()
    print("Database initialized successfully")

if __name__ == "__main__":
    init_db()