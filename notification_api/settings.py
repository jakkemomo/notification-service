from os import environ as env

RABBIT_URL = env.get("RABBIT_URL", "amqp://guest:guest@127.0.0.1:/")
EXCHANGE_NAME = env.get("EXCHANGE_NAME", "notifications")
