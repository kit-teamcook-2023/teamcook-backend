from pydantic import BaseModel
from typing import Optional

class UserSignUp(BaseModel):
    # uid: str
    nickname: str
    address: str
    gasMeter: int
    elecMeter: Optional[int] = None

class Writing(BaseModel):
    title: str
    author: Optional[str]
    content: str

class Clearfirebase(BaseModel):
    isAdmin: str

class Comment(BaseModel):
    post_id: int
    author: Optional[str]
    content: str