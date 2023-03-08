from sqlalchemy.orm import Session

from . import models, schemas
from .hashing import Hasher


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    new_hashed_password = Hasher.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=new_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 

def create_user_title(db: Session, title: schemas.TitleCreate, user_id: int):
    db_item = models.Title(**title.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_user_titles(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Title).filter(models.Title.owner_id == user_id).offset(skip).limit(limit).all()

def create_user_notes(db: Session, title_id: str, note: schemas.NoteCreate, user_id: int):
    db_item = models.Note(**note.dict(), owner_id=title_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_user_notes(db: Session, user_id: int, title_id:int, skip: int = 0, limit: int = 100):
    return db.query(models.Note).filter(models.Note.owner_id == title_id).offset(skip).limit(limit).all()