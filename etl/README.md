## ETL

1. Очередь задач Rabbit MQ
2. Консьюмеры Celery на каждую очередь в rabbit
3. Доп обработка каждой очереди

celery -A tasks worker --loglevel=INFO -Q websocket -n wobsocket
celery -A tasks worker --loglevel=INFO -Q email -n email
