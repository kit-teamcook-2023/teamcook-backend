import asyncio
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, asyncio.Queue] = {}

    def __del__(self):
        for client in self.active_connections:
            del client

    async def connect(self, client_id: str):
        if client_id not in self.active_connections:
            self.active_connections[client_id] = asyncio.Queue()
        return self.active_connections[client_id]

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_event(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].put(message)