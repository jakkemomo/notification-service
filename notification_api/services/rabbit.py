import orjson
from aio_pika import DeliveryMode, Message, RobustConnection
from fastapi import Depends

from notification_api.db.rabbitmq import get_rabbit
from notification_api.settings import EXCHANGE_NAME


class RabbitService:
    def __init__(self, rabbit_conn: RobustConnection):
        self._conn = rabbit_conn

    async def send_message(self, routing_key: str, message: dict):
        encoded_msg = orjson.dumps(message)

        msg = Message(encoded_msg, delivery_mode=DeliveryMode.PERSISTENT)

        async with self._conn.channel() as channel:
            exchange = await channel.get_exchange(EXCHANGE_NAME, ensure=True)
            await exchange.publish(msg, routing_key)


def get_rabbit_service(
    rabbit_conn: RobustConnection = Depends(get_rabbit),
) -> RabbitService:
    return RabbitService(rabbit_conn)
