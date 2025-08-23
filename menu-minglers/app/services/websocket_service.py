# app/services/websocket_service.py
from typing import Dict, List

from fastapi import WebSocket


class WebSocketService:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._clients = set()
        return cls._instance

    @classmethod
    def get_instance(cls) -> "WebSocketService":
        return cls()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self._clients.add(ws)

    def disconnect(self, ws: WebSocket):
        self._clients.discard(ws)

    def get_client_count(self) -> int:
        return len(self._clients)

    async def broadcast_message(self, message: Dict):
        dead = []
        for ws in self._clients:
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)

    async def send_to_client(self, ws: WebSocket, message: Dict):
        await ws.send_json(message)

    def get_client_info(self) -> List[Dict]:
        return [{"id": id(ws)} for ws in self._clients]
