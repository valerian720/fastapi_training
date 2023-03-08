from typing import List
from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from . import crud, models, schemas, security
from .database import SessionLocal, engine
from .config import settings

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 

@app.post("/login/token/", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session= Depends(get_db)):
    user = security.authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

# auth dependency
def get_current_user_from_token(token: str = Depends(oauth2_scheme),db: Session=Depends(get_db)): 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        print("username/email extracted is ",username)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, username)
    if user is None:
        raise credentials_exception
    return user

# 
# users

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# @app.get("/users/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user_from_token)):
    return check_user(user_id, db, current_user)

# titles
@app.post("/users/{user_id}/titles/", response_model=schemas.Title)
def create_title_for_user(user_id: int, title: schemas.TitleCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user_from_token)):
    try:
        check_user(user_id, db, current_user)
    finally:
        return crud.create_user_title(db=db, title=title, user_id=user_id)


@app.get("/users/{user_id}/titles/", response_model=List[schemas.Title])
def read_user_titles(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user_from_token)):
    try:
        check_user(user_id, db, current_user)
    finally:
        titles = crud.get_user_titles(db=db, user_id=user_id, skip=skip, limit=limit)
        return titles

@app.put("/users/{user_id}/titles/", response_model=schemas.Title)
def update_title(user_id: int, title_id: int, title: schemas.TitleCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user_from_token)):
    try:
        check_user(user_id, db, current_user)
        check_title(title_id, db)
    finally:
        return crud.update_title(db=db, title_id=title_id, title=title)
    
@app.delete("/users/{user_id}/titles/")
def delete_title(user_id: int, title_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user_from_token)):
    try:
        check_user(user_id, db, current_user)
        check_title(title_id, db)
    finally:
        return crud.delete_title(db=db, title_id=title_id)


# notes
@app.post("/users/{user_id}/{title_id}/", response_model=schemas.Note)
def create_note_for_user(user_id: int, title_id:int, note: schemas.NoteCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user_from_token)):
    try:
        check_user(user_id, db, current_user)
        check_title(title_id, db)
    finally:
        return crud.create_title_notes(db=db, title_id=title_id, note=note)

@app.get("/users/{user_id}/{title_id}/", response_model=List[schemas.Note])
def read_user_notes(user_id: int, title_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user_from_token)):
    try:
        check_user(user_id, db, current_user)
        check_title(title_id, db)
    finally:
        notes = crud.get_title_notes(db=db, title_id=title_id, skip=skip, limit=limit)
        return notes

@app.put("/users/{user_id}/{title_id}/", response_model=schemas.Note)
def update_note(user_id: int, title_id: int, note_id:int, note: schemas.NoteCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user_from_token)):
    try:
        check_user(user_id, db, current_user)
        check_title(title_id, db)
        check_note(note_id, db)
    finally:
        return crud.update_note(db=db, note_id=note_id, note=note)
    
@app.delete("/users/{user_id}/{title_id}/")
def delete_note(user_id: int, title_id: int, note_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user_from_token)):
    try:
        check_user(user_id, db, current_user)
        check_title(title_id, db)
        check_note(note_id, db)
    finally:
        return crud.delete_note(db=db, note_id=note_id)


# //////////////////////

def check_user(user_id: int, db: Session, current_user: schemas.User):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if db_user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not permitted, your id is <{current_user.id}>")
    return db_user

def check_title(title_id: int, db: Session):
    db_title = crud.get_title(db, title_id=title_id)
    if db_title is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Title not found")
    return db_title

def check_note(note_id: int, db: Session):
    db_note = crud.get_note(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return db_note