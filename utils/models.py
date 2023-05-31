from pydantic import BaseModel
from typing import Optional

class UserSignUp(BaseModel):
    # uid: str
    nickname: str
    address: str
    gasMeter: Optional[int] = None
    elecMeter: Optional[int] = None

class SaveWriting(BaseModel):
    title: str
    content: str
    board: Optional[str]

class Clearfirebase(BaseModel):
    isAdmin: str

class Comment(BaseModel):
    post_id: int
    author: Optional[str]
    content: str

class OCRData(BaseModel):
    dummy: Optional[str]
    ocr_data: str

class PostCommentUpdate(BaseModel):
    id: int | str
    nickname: str
    title: Optional[str]
    content: str