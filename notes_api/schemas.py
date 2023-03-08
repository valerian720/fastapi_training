from typing import List, Union

from pydantic import BaseModel

# ----------------------------- Note
class NoteBase(BaseModel):
    text: str
class NoteCreate(NoteBase):
    pass
class Note(NoteBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True
# ----------------------------- Title
class TitleBase(BaseModel):
    name: str
    is_important: Union[bool, None] = None
    parent_id: Union[int, None] = None
class TitleCreate(TitleBase):
    pass
class Title(TitleBase):
    id: int
    owner_id: int

    notes: List[Note] = []
    # parent: TitleBase # ???
    class Config:
        orm_mode = True

# ----------------------------- User

class UserBase(BaseModel):
    email: str
class UserCreate(UserBase):
    password: str
class User(UserBase):
    id: int
    is_active: bool
    titles: List[Title] = []

    class Config:
        orm_mode = True
# ----------------------------- Token

class Token(BaseModel):
    access_token: str
    token_type: str