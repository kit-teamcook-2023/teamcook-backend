from fastapi import FastAPI, HTTPException, WebSocketException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.websockets import WebSocketState
import asyncio

from utils.sse import ConnectionManager

app = FastAPI()
active_connections = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


manager = ConnectionManager()

@app.get("/connect/{client_id}")
async def connect(client_id: str):
    queue = await manager.connect(client_id)

    async def event_stream():
        try:
            while True:
                message = await queue.get()
                yield f"data:{message}\n\n"
        except asyncio.CancelledError:
            manager.disconnect(client_id)

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/")
async def healthcheck():
    return {"status": "ok"}

@app.get("/disconnect/{client_id}")
async def disconnect(client_id: str):
    manager.disconnect(client_id)
    return {"status": "disconnected"}

@app.get("/send_event/{client_id}")
async def send_event(client_id: str):
    await manager.send_event("Some event data", client_id)
    return {"status": "event sent"}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    users = ["10", "20"]
    room_address = "10-20"
    await websocket.accept()
    add_user_to_chat_room(room_address, websocket)
    try:
        for user_id in users:  # 여기서 "B"는 다른 사용자의 ID입니다.
            if user_id == client_id:
                idx = users.index(user_id)
                await manager.send_event(f"A new chat room {room_address} has been created!", users[1-idx])
        while True:
            data = await websocket.receive_text()
            human, data = map(str, data.replace(" ", "").split(":"))
            await send_message_to_chat_room(room_address, data, websocket)


    except Exception:
        # WebSocket 연결이 종료되면 사용자를 채팅방에서 제거
        remove_user_from_chat_room(room_address, websocket)
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close()

# 채팅방에 메시지 전송
async def send_message_to_chat_room(room_address: str, message: str, mysocket: WebSocket):
    if room_address in active_connections:
        for socket in active_connections[room_address]:
            if socket is not mysocket:
                await socket.send_text(message)

# 채팅방에 사용자 추가
def add_user_to_chat_room(room_address: str, websocket: WebSocket):
    if room_address not in active_connections:
        active_connections[room_address] = []
    active_connections[room_address].append(websocket)

# 채팅방에서 사용자 제거
def remove_user_from_chat_room(room_address: str, websocket: WebSocket):
    if room_address in active_connections:
        active_connections[room_address].remove(websocket)