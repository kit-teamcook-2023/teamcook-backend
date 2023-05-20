from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocketState
import pymysql

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

active_connections = {}
db = pymysql.connect(host="localhost", user="database", password="database", database="chatting")


# 채팅방에 입장하는 WebSocket 연결 처리
@app.websocket("/chat/{uid1}-{uid2}")
async def websocket_endpoint(uid1: str, uid2: str, websocket: WebSocket):
    await websocket.accept()

    # 채팅방 주소 생성
    room_address = f"{uid1}-{uid2}"
    if not room_exisits(room_address):
        create_room(room_address)
    print(room_address)

    # 채팅방에 사용자 추가
    add_user_to_chat_room(room_address, websocket)
    print("append complete")

    try:
        while True:
            # 클라이언트로부터 메시지 수신
            data = await websocket.receive_text()

            # 테스트로는 sender: data 형식으로 받아올 예정
            human, data = map(str, data.replace(" ", "").split(":"))

            # 메시지 전송
            await send_message_to_chat_room(room_address, data, websocket)

            # 메시지 백업
            backup_message(room_address, data, human)

    except Exception:
        # WebSocket 연결이 종료되면 사용자를 채팅방에서 제거
        remove_user_from_chat_room(room_address, websocket)
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close()


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


# 메시지 백업
def backup_message(room_address: str, message: str, sender: str):
    try:
        with db.cursor() as cursor:
            # chat_log 테이블에 메시지 백업
            sql = "INSERT INTO chat_log (room_name, message, sender) VALUES (%s, %s, %s)"
            cursor.execute(sql, (room_address, message, sender))
        db.commit()
    except Exception as e:
        print(f"Error occurred during message backup: {e}")
        db.rollback()

def room_exisits(room_address: str) -> bool:
    with db.cursor() as cursor:
        sql = f"""SELECT COUNT(*) FROM room_info WHERE `room_name`='{room_address}'"""
        cursor.execute(sql)
        res = cursor.fetchone()
    return True if res[0] == 1 else False

def create_room(room_address: str):
    try:
        with db.cursor() as cursor:
            sql = f"""INSERT INTO room_info(room_name) VALUES ('{room_address}')"""
            cursor.execute(sql)
        db.commit()
    except:
        None
        
def find_nickname_using_uid(uid: str) -> str:
    with db.cursor() as cursor:
        sql = f"""SELECT nickname FROM nicknames WHERE `uid`='{uid}'"""
        cursor.execute(sql)
        res = cursor.fetchone()
    return res[0]

@app.get("/chatting/{chatting_room_id}/chat")
def get_previous_chat(chatting_room_id: str):
    try:
        with db.cursor() as cursor:
            sql = f"""SELECT * FROM chat_log WHERE `room_name`='{chatting_room_id}'"""
            cursor.execute(sql)
            res = cursor.fetchall()
    except:
        res = []
    return res