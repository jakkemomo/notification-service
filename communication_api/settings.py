from os import environ as env

RABBIT_URL = env.get("RABBIT_URL", "amqp://user:password@127.0.0.1:/")
EXCHANGE_NAME = env.get("EXCHANGE_NAME", "notifications")

MONGO_URI = env.get("MONGO_URI", "mongodb://127.0.0.1:27017/")
MONGO_DB = env.get("MONGO_DB", "movies")
