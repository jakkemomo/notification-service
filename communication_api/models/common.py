from enum import Enum


class MsgTypes(str, Enum):
    EMAIL = "email"
    WEBSOCKET = "websocket"
