from typing import Optional

from aio_pika import RobustConnection

rabbit_conn: Optional[RobustConnection] = None


def get_rabbit() -> RobustConnection:
    return rabbit_conn
