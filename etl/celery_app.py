from celery import Celery

broker_url = "amqp://localhost:5672"
redis_url = "redis://localhost:6380"
app = Celery("tasks", broker=broker_url, backend=redis_url)
app.conf.task_routes = {
    'email.*': {'queue': 'email'},
    'websocket.*': {'queue': 'websocket'},
}
