from enum import Enum
from typing import List, Union
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()
# 
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
# 
@app.get("/")
async def root():
    return {"message": "welcome to API, check out /docs on this host"}
# 
