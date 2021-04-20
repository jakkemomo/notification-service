#!/bin/sh

if [ "$database" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $db_host $db_port; do
      sleep 0.1
    done

    echo "PostgreSQL started"

fi

sleep 3

python /usr/src/admin_panel/manage.py flush --no-input
python /usr/src/admin_panel/manage.py migrate
python /usr/src/admin_panel/manage.py loaddata fixture.json
python /usr/src/admin_panel/manage.py collectstatic --no-input --clear

mkdir -p ~/.clickhouse-client /usr/local/share/ca-certificates/Yandex && \
wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" -O /usr/local/share/ca-certificates/Yandex/YandexInternalRootCA.crt && \
wget "https://storage.yandexcloud.net/mdb/clickhouse-client.conf.example" -O ~/.clickhouse-client/config.xml

python3 manage.py runapscheduler &

exec "$@"
