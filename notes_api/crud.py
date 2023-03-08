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

# Create / ReadMany / readOne / Update / Delete 

def create_user_title(db: Session, title: schemas.TitleCreate, user_id: int):
    db_title = models.Title(**title.dict(), owner_id=user_id)
    db.add(db_title)
    db.commit()
    db.refresh(db_title)
    return db_title

def get_user_titles(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Title).filter(models.Title.owner_id == user_id).offset(skip).limit(limit).all()

def get_title(db: Session, title_id: int):
    return db.query(models.Title).filter(models.Title.id == title_id).first()

def update_title(db: Session, title_id: int, title: schemas.TitleCreate):
    db_title = get_title(db=db, title_id=title_id)
    title_data = title.dict(exclude_unset=True)
    for key, value in title_data.items():
        setattr(db_title, key, value)
    db.add(db_title)
    db.commit()
    db.refresh(db_title)
    return db_title

def delete_title(db: Session, title_id: int):
    db_title = get_title(db=db, title_id=title_id)
    db.delete(db_title)
    db.commit()
    return {"ok": True}

#  Create / ReadMany / readOne / Update / Delete 

def create_title_notes(db: Session, title_id: str, note: schemas.NoteCreate):
    db_note = models.Note(**note.dict(), owner_id=title_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_title_notes(db: Session, title_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Note).filter(models.Note.owner_id == title_id).offset(skip).limit(limit).all()

def get_note(db: Session, note_id: int):
    return db.query(models.Note).filter(models.Note.id == note_id).first()

def update_note(db: Session, note_id: int, note: schemas.NoteCreate):
    db_note = get_note(db=db, note_id=note_id)
    note_data = note.dict(exclude_unset=True)
    for key, value in note_data.items():
        setattr(db_note, key, value)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def delete_note(db: Session, note_id: int):
    db_note = get_note(db=db, note_id=note_id)
    db.delete(db_note)
    db.commit()
    return {"ok": True}