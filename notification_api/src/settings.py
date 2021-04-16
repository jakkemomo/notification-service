from os import environ as env

MONGO_URI = env.get("MONGO_URI", "mongodb://127.0.0.1:27017/")
MONGO_DB = env.get("MONGO_DB", "movies")

AUTH_DEBUG = env.get("AUTH_DEBUG", 0)
USER_ID_DEBUG = env.get("USER_ID_DEBUG", "user-12345")
AUTH_URI = env.get("AUTH_URI", "http://127.0.0.1:8000/api/v1/pubkey")
