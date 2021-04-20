from enum import Enum


class DeliveryType(Enum):
    email = "email"
    websocket = "websocket"


class ContentType(Enum):
    news = "news"
    recommendation = "recommendation"
