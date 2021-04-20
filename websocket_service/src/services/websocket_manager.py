import copy
import logging
from collections import defaultdict
from functools import lru_cache
from typing import DefaultDict, List

from fastapi import WebSocket
from websockets.exceptions import ConnectionClosed

logger = logging.getLogger(__name__)


class WebsocketManager:
    def __init__(self):
        self.active_connections: DefaultDict[str, List[WebSocket]] = defaultdict(list)

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id].append(websocket)
        logger.info("User [%s] has created connection" % user_id)

    def disconnect(self, user_id: str, websocket: WebSocket):
        self.active_connections[user_id].remove(websocket)
        logger.info("One of user [%s] connection is closed" % user_id)

    async def send_message(self, user_id: str, message: str):
        user_connections = copy.copy(self.active_connections[user_id])
        for ws in user_connections:
            try:
                await ws.send_text(message)
            except ConnectionClosed:
                self.disconnect(user_id, ws)


@lru_cache
def get_websocket_manager() -> WebsocketManager:
    return WebsocketManager()
