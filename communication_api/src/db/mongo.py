from typing import Optional

from motor.core import AgnosticClient

mongo_conn: Optional[AgnosticClient] = None


def get_mongo_conn() -> AgnosticClient:
    return mongo_conn
