import asyncio

from fastapi import APIRouter, Depends, Header, WebSocket, status
from pydantic import BaseModel

from websocket_service.src.services.auth import get_websocket_user
from websocket_service.src.services.websocket_manager import (
    WebsocketManager,
    get_websocket_manager,
)
from websocket_service.src.settings import settings

SLEEP_TIME = settings.sleep_time

ws_router = APIRouter()


class MessageIn(BaseModel):
    message: str


@ws_router.post("/notifications/{user_id}")
async def send_notification(
    user_id: str,
    message: MessageIn,
    ws_manager: WebsocketManager = Depends(get_websocket_manager),
):
    await ws_manager.send_message(user_id, message.message)


@ws_router.websocket("/ws/notifications")
async def websocket_endpoint(
    ws: WebSocket,
    ws_manager: WebsocketManager = Depends(get_websocket_manager),
    authorization: str = Header(None),
):
    user = await get_websocket_user(authorization)
    if not user:
        await ws.close(code=status.WS_1008_POLICY_VIOLATION)

    await ws_manager.connect(user.id, ws)

    # I have to use the infinite loop to the socket does not close
    while True:
        await asyncio.sleep(SLEEP_TIME)
