from os import environ as env

RABBIT_URI = env.get("RABBIT_URL", "amqp://user:password@127.0.0.1:/")
EXCHANGE_NAME = env.get("EXCHANGE_NAME", "notifications")

MONGO_URI = env.get("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = env.get("MONGO_DB", "movies")

CELERY_CONF = env.get("CELERY_CONF", "celery_conf")

NOTIFICATION_API_HOST = env.get("NOTIFICATION_API_HOST", "localhost")
NOTIFICATION_API_PORT = env.get("NOTIFICATION_API_PORT", 80)

DELIVERY_TYPE_TASKS = {
    "email": "process_email_query",
    "websocket": "process_websocket_query",
}
