from enum import Enum


class DeliveryType(str, Enum):
    email = "email"
    websocket = "websocket"


class ContentType(str, Enum):
    news = "news"
    recommendation = "recommendation"
