from enum import Enum


class DeliveryType(str, Enum):
    EMAIL = "email"
    WEBSOCKET = "websocket"


class ContentType(str, Enum):
    NEWS = "news"
    RECOMMENDATION = "recommendation"
