from os import environ as env

MONGO_URI = env.get("MONGO_URI", "mongodb://127.0.0.1:27017/")
MONGO_DB = env.get("MONGO_DB", "movies")
