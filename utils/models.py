from pydantic import BaseModel
from typing import Optional

class UserSignUp(BaseModel):
    # uid: str
    nickname: str
    address: str
    gasMeter: Optional[int | str] = None
    elecMeter: Optional[int | str] = None

    class Config:
        schema_extra = {
            "example": {
                "nickname": "nickname",
                "address": "테스트주소1",
                "gasMeter": "Optional[int | str]. 회원가입시 받을 수 있으면 최고",
                "elecMeter": "Optional[int | str]. 회원가입시 받을 수 있으면 최고"
            }
        }

class SaveWriting(BaseModel):
    title: str
    content: str
    board: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "글 제목",
                "content": "글 내용",
                "board": "free | group-buying | etc. | None"
            }
        }

class Clearfirebase(BaseModel):
    isAdmin: str

class Comment(BaseModel):
    post_id: int
    author: Optional[str]
    content: str

    class Config:
        schema_extra = {
            "example": {
                "post_id": 10,
                "author": "작성자 닉네임, 토큰으로 얻을 수 있어서 필수 아님",
                "content": "댓글 내용"
            }
        }

class OCRData(BaseModel):
    dummy: Optional[str]
    ocr_data: str | int

    class Config:
        schema_extra = {
            "example": {
                "dummy": "dummy 데이터. 필수 아님",
                "ocr_data": "ocr 판독 결과"
            }
        }

class PostCommentUpdate(BaseModel):
    id: int | str
    nickname: str
    title: Optional[str]
    content: str

    class Config:
        schema_extra = {
            "example": {
                "id": "글/댓글 id",
                "nickname": "자신의 닉네임. 본인이 맞는지 토큰과 비교하는 용도",
                "title": "글 수정일 경우에만 전달. 글 제목",
                "content": "글/댓글 내용"
            }
        }

class NicknameUpdate(BaseModel):
    nickname: str

    class Config:
        schema_extra = {
            "example": {
                "nickname": "user_inputted_nickname"
            }
        }