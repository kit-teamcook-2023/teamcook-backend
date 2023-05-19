from pydantic import BaseModel
from typing import Optional

class UserSignUp(BaseModel):
    # uid: str
    nickname: str
    address: str
    gasMeter: Optional[int] = None
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

class OCRData(BaseModel):
    dummy: Optional[str]
    ocr_data: str