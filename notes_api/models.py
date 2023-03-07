from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

"""
Список таблиц для приложения для создания заметок
- User
- Title
- Note

user owns many titles
title owns many titles
title owns many notes

"""

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)
    # meta
    titles = relationship("Title", back_populates="user_owner") # child link

class Title(Base):
    __tablename__ = "titles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    is_important = Column(Boolean, default=True)
    parent_id = Column(Integer, ForeignKey('titles.id'))
    owner_id = Column(Integer, ForeignKey("users.id"))
    # meta
    children_title = relationship('Title', remote_side='Title.id') # self link
    user_owner = relationship("User", back_populates="titles") # parent link
    notes = relationship("Note", back_populates="title_owner") # child link


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(500))
    owner_id = Column(Integer, ForeignKey("titles.id"))
    # meta
    title_owner = relationship("Title", back_populates="notes") # parent link




