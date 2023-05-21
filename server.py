# firebase 데이터베이스에 접근하기 위한 클래스
from database.firebase import Firebase

# 게시판 데이터베이스에 접근하기 위한 클래스
from database.user_sql import UserSQL
from database.chat_sql import ChatSQL

# 서버 구축을 위한 fastapi
from fastapi import FastAPI, Depends, Header, status, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.websockets import WebSocketState
from typing import Optional
# from pydantic import BaseModel

from datetime import datetime
from dateutil.relativedelta import relativedelta
import httpx
import os
from dotenv import load_dotenv
import json

from utils.responces import Responces
from utils.models import UserSignUp, SaveWriting, Clearfirebase, Comment, OCRData
from auth.auth_handler import signJWT, decodeJWT
from auth.auth_bearer import JWTBearer
load_dotenv(verbose=True)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CLEAR_DB_KEY = os.getenv('CLEAR_DB_KEY')

app = FastAPI()
firebase = Firebase() # credential은 호출하는 파일의 디렉터리에 있어야한다!
sql_user = UserSQL()
sql_chat = ChatSQL()
res = Responces()


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://34.215.66.235:8000",
]

allow_methods = [
    "GET",
    "POST",
    "PUT",
    "DELETE"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=allow_methods,
    allow_headers=["*"],
)
# root. responce 확인용
@app.get("/", tags=["Hello World!"],
         status_code=status.HTTP_200_OK)
async def root(request: Request):
    return {"title": "hello world"}


# params로 fee 받아옴
@app.post("/gas-meter/{uid}")
async def get_gas_meter(uid: str, item: OCRData):
    uid = uid.strip()
    # OCRData일 경우에는 item.ocr_data
    # OCRData.dict() 한 경우에는 item['ocr_data']
    item = item.dict()
    gas_meter = item['ocr_data']
    print(uid, gas_meter)
    # firebase.push(uid, "gas", gas_meter)
    return JSONResponse(status_code=status.HTTP_200_OK, content=item)

# @app.get("/test-for-pi", tags=["test"])
# async def testing():
#     async with httpx.AsyncClient() as client:
#         response = await client.get("http://choijungwoo.iptime.org:5000/ocr", data={

#         })
#     None

# get? post?
# front와 협의 필요
# 사용자의 uid와 년도-달-일 을 이용하여 전기사용량, 가스사용량 획득
@app.get("/user-fee", tags=["사용자 정보"],
         dependencies=[Depends(JWTBearer())],
         description="사용자의 uid와 년도-달-일 을 이용하여 전기사용량, 가스사용량 획득",
         responses=res.get_user_fee())
# date:str, 
async def get_gas_elec(Authorization: Optional[str] = Header(None)):
    payload = decodeJWT(Authorization[7:])
    uid = payload['uid']
    today = datetime.today().strftime("%y-%m-%d-%H")
    date = today
    # print(date)
    # today = date

    # 시작일 알려줌
    year, month, day, hour = [int(part) for part in date.split("-")]

    # start_of_cur_month = datetime(year=year, month=month, day=1, hour=hour).strftime("%y-%m-%d-%H")
    start_of_cur_month = date

    # 저번달 시작일 알려줌
    start_of_last_month = datetime(year=year, month=month, day=day, hour=hour-1).strftime("%y-%m-%d-%H")

    # data_now = request to raspberry pi
    ip = firebase.get_user_ip(uid)
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ip}/ocr")
        data = response.json()

    data_now = {
        'gas': data['ocr_data']
    }


    # 아래는 임시 데이터 적용
    # data_now = {
    #     'gas': 180,
    #     'elec': 700
    # }
    data_cur = firebase.search(uid, start_of_cur_month)
    data_last = firebase.search(uid, start_of_last_month)
    rate_cur = firebase.search('rating', start_of_cur_month)
    rate_last = firebase.search('rating', start_of_last_month)

    ret = {
        'last_month': calc_fees(data_cur, data_last, rate_last),
        'cur_month' : calc_fees(data_now, data_cur, rate_cur)
    }

    
    return JSONResponse(status_code=status.HTTP_200_OK, content=ret)

def calc_fees(cur: dict, last: dict, rate:dict) -> dict:
    gas_diff = cur['gas'] - last['gas']
    # elec_diff = cur['elec'] - last['elec']

    # elec_rates = list(rate['elec'].keys())

    ret = {
        'gas': calc_gas_fee(gas_diff, rate['gas']),
        # 'elec': calc_elec_fee(elec_diff, elec_rates, rate['elec'])
    }

    return ret

def calc_elec_fee(diff: int, rates_keys: list, rate: dict) -> int: # 완성
    elec_fee = 0

    global_weather_fee = diff * 9
    fuel_locale = diff * 5

    if diff <= int(rates_keys[0]):
        elec_fee += rate[rates_keys[0]]['base']
        elec_fee += diff * rate[rates_keys[0]]['rate']
    elif diff <= int(rates_keys[1]):
        elec_fee += rate[rates_keys[1]]['base']
        elec_fee += diff * rate[rates_keys[0]]['rate']
        diff -= int(rates_keys[0])
        elec_fee += diff * rate[rates_keys[1]]['rate']
    else:
        elec_fee += rate[rates_keys[2]]['base']
        elec_fee += diff * rate[rates_keys[0]]['rate']
        diff -= int(rates_keys[0])
        elec_fee += diff * rate[rates_keys[1]]['rate']
        diff -= int(rates_keys[1])
        elec_fee += diff * rate[rates_keys[1]]['rate']

    elec_fee = elec_fee + global_weather_fee + fuel_locale
    electrivcity_base_fee = int(elec_fee * 0.037)

    elec_fee = int(elec_fee * 1.1 + electrivcity_base_fee)
    return elec_fee

def calc_gas_fee(diff: int, rate: int) -> int:
    mj = diff * 43 * 0.9893
    fee = mj * rate
    gas_fee = (fee+1000)*1.1

    return int(gas_fee)

# 유저 닉네임이 사용중인지 확인 
@app.get("/is-nick-use", tags=["사용자 정보"],
         description="유저 닉네임이 사용중인지 확인",
         responses=res.check_nickname_usage())
def is_user_in(nickname: str):
    if sql_user.searchNickname(nickname) == True:
        return JSONResponse(status_code=status.HTTP_226_IM_USED)
    else:
        return JSONResponse(status_code=status.HTTP_200_OK)

# get? post?
# 사용자가 회원가입을 한 경우 실행
# rest api 사용하지만 get 쓰든 post 쓰든 알빠노?긴 함
# post로 받을 것
# 라즈베리파이에 request 보내서 가스 사용량, 전기 사용량 획득하여 데이터베이스에 저장
@app.post("/signup", tags=["사용자 정보"],
          dependencies=[Depends(JWTBearer())],
           responses=res.sign_up(),
          description="회원가입한 유저의 데이터를 서버 데이터베이스에 저장. 닉네임, 사용자 가스, 전기 사용량을 저장")
async def signup(user: UserSignUp, Authorization: Optional[str] = Header(None)):
    nickname = user.nickname
    address = user.address
    gasmeter = user.gasMeter

    payload = decodeJWT(Authorization[7:])
    uid = payload['uid']
    domain = sql_user.getDomainFromAddress(address)
    if sql_user.searchNickname(nickname):
        return JSONResponse(status_code=status.HTTP_226_IM_USED, content={"signup": "ignored"})
    
    try:
        res = await init_pi(domain, uid, "append")
    except:
        res = {'gas': 300}
    
    firebase.push(uid=uid, type="nickname", data=nickname)
    firebase.push(uid=uid, type="ip", data=domain)
    gasmeter = int(gasmeter)
    firebase.push(uid=uid, type="gas", data=['', res['gas']])
    sql_user.appendNickname(nickname, uid)

    # DELETE FROM nicknames WHERE nickname='test10';


    firebase.create_user({
        'uid': uid,
        'nickname': nickname
    })

    return JSONResponse(status_code=status.HTTP_200_OK, content=signJWT(nickname, uid, 30 * 24 * 60 * 60))

    # 라즈베리파이에 get 요청

    # if user.gasMeter == None:
    #   get method to gas meter

    # if user.elecMeter == None:
    #   get method to elec meter


    # 얻은 데이터를 데이터베이스에 저장
    # push(uid, type='', data='', date='')
    # firebase.push(user.uid, type='', data='', date='', nickname=nickname.hexdigest())
    # firebase.push(uid, type='gas', data=gasdata, date=d, nickname='')
    # firebase.push(uid, type='elec', data=elecdata, date=d, nickname='')

    # 전 달 데이터와 비교하여 차이 계산 필요

    # 값 반환
    return "asdf"

async def init_pi(domain: str, uid: str, command: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(domain+"/init", data={
            "uid": uid,
            "command": command
        })

    return response.json()

@app.delete("/deleteaccount", tags=["사용자 정보"],
          dependencies=[Depends(JWTBearer())],
          responses=res.delete_user()
        )
async def deleteAccount(Authorization: Optional[str] = Header(None)):
    token = decodeJWT(Authorization[7:])
    payload = token
    uid = payload['uid']

    domain = firebase.get_user_ip(uid)
    try:
        _ = await init_pi(domain, uid, "remove")
    except:
        None

    res = firebase.delete_user(uid)
    # nickname = payload['nickname']
    try:
        sql_user.deleteUser(uid)
        # sql_user.deleteUser(nickname)
    except:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
            'status': 'already deleted - sql_user'
        })
    if res:
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            'status': 'delete successed'
        })
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
            'status': 'already deleted - firebase'
        })


# 게시판 데이터베이스 관련
@app.get("/search-posts", tags=["게시판"],
         description="게시글 검색",
         responses=res.search_posts())
# responce 추가 필요
def searchPosts(type:str, data:str, page:int, board: Optional[str] = None):
    # print(type, data, page)
    
    count = sql_user.getSearchWritingsCount(type, data, board)
    posts = sql_user.searchWriting(type, data, page, board)
    ret = {
        'post_counts': count['row_count'],
        'posts': posts
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=ret)

@app.get("/all-posts", tags=["게시판"],
         description="전체 게시글 반환",
         responses=res.get_all_posts())
def getAllPosts(board: Optional[str] = None):
    result = sql_user.getAllWritings(board)
    rows = sql_user.getWritingsCount(board)['row_count']
    ret = {
        'counts': rows,
        'posts': result
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=ret)

@app.get("/post", tags=["게시판"],
         description="게시글 조회",
         responses=res.get_post())
def getPostAndComments(id:int):
    ret = {}
    result = sql_user.getWriting(id=id)
    try:
        ret['writing'] = result['write']
        ret['writing_id'] = result['parent']
    except:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
            "status": "Not exist post id"
        })
        # ret['writing'] = {}

    try:
        result = sql_user.getComments(id)
        ret['comments'] = result
    except:
        ret['comments'] = {}

    return JSONResponse(status_code=status.HTTP_200_OK, content=ret)

@app.post("/post", tags=["게시판"],
          dependencies=[Depends(JWTBearer())],
         description="게시글 작성",
         responses=res.post_post())
def insertPostToMysql_user(writing: SaveWriting, Authorization: Optional[str] = Header(None)):
    payload = decodeJWT(Authorization[7:])

    # author = writing.author
    author = payload['nickname']
    title = writing.title
    content = writing.content
    board = None
    if writing.board:
        board = writing.board

    try:
        sql_user.appendWriting(title,content,author,board)
        id = sql_user.getLastPost(author)
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "id": id,
            "status": "Post post successed"
        })
    except:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
            "status": "Post post failed"
        })

@app.post("/comment", tags=["게시판"],
         description="댓글 작성",
         responses=res.post_comment())
def insertCommentToMysql_user(comment: Comment, Authorization: Optional[str] = Header(None)):
    payload = decodeJWT(Authorization[7:])
    author = payload['nickname']
    content = comment.content
    post_id = comment.post_id
    title = "" # 미래에 사용할 수도 있음

    try:
        sql_user.appendComment(title, content, author, post_id)
        comment_id = sql_user.getLastComment(author)
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "comment_id": comment_id,
            "post_id": post_id,
            "status": "Post comment successed"
        })
    except:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
            "status": "Post comment failed"
        })

# delete는 uri 형식으로 값을 받아온다.
@app.delete("/post/{id}/{nickname}", tags=["게시판"],
        dependencies=[Depends(JWTBearer())],
         description="글 삭제",
         responses=res.delete("post"))
def removePostFromMysql_user(id:int , nickname: str, Authorization: Optional[str] = Header(None)):
    payload = decodeJWT(Authorization[7:])
    # if payload['nickname'] != element.nickname:
    if payload['nickname'] != nickname:
        return JSONResponse(status_code=status.HTTP_401_BAD_REQUEST, content={
            "status": "Not allowed"
        })
    
    try:
        sql_user.deleteWriting(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "status": "Remove post successed"
        })
    except:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
            "status": "Remove post failed"
        })

@app.delete("/comment/{id}/{nickname}", tags=["게시판"],
         description="댓글 삭제",
         dependencies=[Depends(JWTBearer())],
         responses=res.delete("comment"))
def removeCommentFromMysql_user(id:int , nickname: str, Authorization: Optional[str] = Header(None)):
    payload = decodeJWT(Authorization[7:])
    if payload['nickname'] != nickname:
        return JSONResponse(status_code=status.HTTP_401_BAD_REQUEST, content={
            "status": "Not allowed"
        })
    
    try:
        sql_user.deleteComment(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "status": "Remove comment successed"
        })
    except:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
            "status": "Remove comment failed"
        })

@app.get("/auth/kakao/callback", tags=["카카오 인증 콜백"],
    responses=res.kakao_callback())
async def kakao_callback(request: Request, code: str):
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET
    redirect_uri = "http://15.165.65.93/auth/kakao/callback"
    # redirect_uri = "http://localhost:3000/auth/kakao/callback"
    token_url = "https://kauth.kakao.com/oauth/token"
    user_info_url = "https://kapi.kakao.com/v2/user/me"
    
    # 액세스 토큰 요청
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data={
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "code": code
        })
    access_token = response.json().get("access_token")

    # 사용자 정보 요청
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get(user_info_url, headers=headers)
    user_info = response.json()

    # user_info에 있는 uid값은 int형이었다..!
    uid = str(user_info.get("id"))
    res_code, nickname = firebase.get_user_kakao(uid)
    # print(res_code)
    if res_code == True:
        return JSONResponse(status_code=status.HTTP_226_IM_USED, content=signJWT(nickname, uid, 30 * 24 * 60 * 60))
    else:
        return JSONResponse(status_code=status.HTTP_200_OK, content=signJWT(nickname, uid, 10 * 60))

@app.get("/auth/google/callback")
async def google_callback():
    None

@app.get("/check-jwt", tags=["토큰 유효성 검사"], dependencies=[Depends(JWTBearer())],
    responses=res.check_valid_token())
async def checkJWT(Authorization: str = Header(None)):
    return JSONResponse(status_code=status.HTTP_200_OK, content={
            'status':'vaild'
        })

@app.get('/test', tags=["test"])
async def test(uid):
    uid = str(uid)
    ip: str = await firebase.get_user_ip(uid)
    if ip[0] != 'h':
        ip = 'http://'+ip
    ip += 'camera' if ip[-1] == '/' else '/camera'
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(ip)
            response.raise_for_status()
    except (httpx.TimeoutException, httpx.HTTPStatusError) as e:
        return "timed out"
    return response.text
    # keys = list(firebase.search_nickname('').keys())
    # if 'fgh' in keys:
    #     return JSONResponse(status_code=status.HTTP_226_IM_USED)
    #     return status.HTTP_226_IM_USED
    # else:
    #     return JSONResponse(status_code=status.HTTP_200_OK)
    #     return status.HTTP_200_OK

@app.put('/clear_db', tags=["clear_db"])
def clearfirebase(cls:Clearfirebase):
    if cls.isAdmin == CLEAR_DB_KEY:
        sql_user.clearDatabase()
        return status.HTTP_200_OK
    return status.HTTP_400_BAD_REQUEST

@app.get("/test-kakao/{uid}", tags=["test"])
def test_kakao(uid:int):
    data = {
        'uid': str(uid),
        'nickname': 'test1'
    }
    firebase.create_user(data)

    return firebase.get_user_kakao(str(uid))

@app.get("/prev-chat/{user_nickname}", tags=["chatting"], dependencies=[Depends(JWTBearer())],
         responses=res.get_previous_chat())
def get_previous_chat_test(user_nickname: str, Authorization: str = Header(None)):
    payload = decodeJWT(Authorization[7:])
    uid = int(payload['uid'])
    other_uid = int(sql_user.findUidUSENickname(user_nickname))

    chatting_room_id = make_chatting_room_id(uid, other_uid)
    
    return sql_chat.get_previous_chat(chatting_room_id)


# @app.get("/prev-chat/{chatting_room_id}", tags=["chatting", "websocket"])
# def get_previous_chat(chatting_room_id: str):
#     return sql_chat.get_previous_chat(chatting_room_id)

active_connections = {}
# 채팅방에 입장하는 WebSocket 연결 처리
@app.websocket("/chat/{my_uid}/{opo_nickname}")
async def websocket_endpoint(my_uid: str, opo_nickname: str, websocket: WebSocket):
    await websocket.accept()
    # 채팅방 주소 생성
    other_uid = int(sql_user.findUidUSENickname(opo_nickname))
    uid = int(my_uid)

    my_nickname = sql_user.findNicknameUSEUid(my_uid)

    chatting_room_id = make_chatting_room_id(uid, other_uid)

    if not sql_chat.room_exisits(chatting_room_id):
        sql_chat.create_room(chatting_room_id)

    # 채팅방에 사용자 추가
    add_user_to_chat_room(chatting_room_id, websocket)

    try:
        while True:
            # 클라이언트로부터 메시지 수신
            data = await websocket.receive_text()

            # 테스트로는 sender: data 형식으로 받아올 예정
            human, data = split_chatting_message(data)

            # 메시지 전송
            await send_message_to_chat_room(chatting_room_id, data, websocket)

            # 메시지 백업
            sql_chat.backup_message(chatting_room_id, data, human)

    except Exception:
        # WebSocket 연결이 종료되면 사용자를 채팅방에서 제거
        remove_user_from_chat_room(chatting_room_id, websocket)
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close()

def make_chatting_room_id(uid: str, opo_uid: str):
    uid = int(uid)
    opo_uid = int(opo_uid)
    return f"""{uid}-{opo_uid}""" if uid < opo_uid else f"""{opo_uid}-{uid}"""

# 채팅 구분
def split_chatting_message(message: str):
    temp = message.replace(" ", "").split(":")
    if len(temp) == 1:
        human = "testing_____"
        data = temp[0]
    else:
        human, data = map(str, temp)
    
    return human, data

# 채팅방에 사용자 추가
def add_user_to_chat_room(room_address: str, websocket: WebSocket):
    if room_address not in active_connections:
        active_connections[room_address] = []
    active_connections[room_address].append(websocket)


# 채팅방에서 사용자 제거
def remove_user_from_chat_room(room_address: str, websocket: WebSocket):
    if room_address in active_connections:
        active_connections[room_address].remove(websocket)


# 채팅방에 메시지 전송
async def send_message_to_chat_room(room_address: str, message: str, mysocket: WebSocket):
    if room_address in active_connections:
        for socket in active_connections[room_address]:
            if socket is not mysocket:
                await socket.send_text(message)