from sqlalchemy.orm import Session
from app.db.models.user import User
from app.utils.security import hash_password

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, username: str, email: str, password: str):
    db_user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, username: str = None, email: str = None):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        if username:
            db_user.username = username
        if email:
            db_user.email = email
        db.commit()
        db.refresh(db_user)
    return db_user