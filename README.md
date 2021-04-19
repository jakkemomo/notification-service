# Проектная работа 10 спринта

Проектные работы в этом модуле выполняются в одиночку, без деления на команды. Задания на спринт вы найдёте внутри тем.

Для настройки монго в сервисе нотификации надо выполнить:

    Из директории notification_api

    docker-compose up -d
    docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}]})" | mongo'
    docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}]})" | mongo'
    docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongo'


Для загрузки шаблонов писем в админку необходимо выполнить:

     python3 admin_panel/manage.py loaddata fixture.json

Для создания очередей в ETL необходимо запустить:

    celery -A etl.tasks worker --loglevel=INFO -Q websocket -n wobsocket
    celery -A etl.tasks worker --loglevel=INFO -Q email -n email
