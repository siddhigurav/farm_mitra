from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import asyncio
import json


class ConnectionManager:
    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active.append(websocket)

    def disconnect(self, websocket: WebSocket):
        try:
            self.active.remove(websocket)
        except ValueError:
            pass

    async def send_personal(self, websocket: WebSocket, message: dict):
        await websocket.send_json(message)

    def broadcast(self, message: dict):
        # schedule broadcast to all active websockets
        for ws in list(self.active):
            asyncio.create_task(self._safe_send(ws, message))

    async def _safe_send(self, ws: WebSocket, message: dict):
        try:
            await ws.send_json(message)
        except Exception:
            self.disconnect(ws)


manager = ConnectionManager()
