#!/bin/bash

>&2 echo "Starting Celery workers"

celery -A /usr/src/etl/tasks worker --loglevel=INFO -Q websocket -n wobsocket
celery -A /usr/src/etl/tasks worker --loglevel=INFO -Q email -n email

exec "$@"
