import logging
from datetime import datetime, timedelta

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from clickhouse_driver import Client
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore

from admin_panel.mails.sql_queries import (
    SQL_USER_IDS,
    SQL_VIEWS,
    SQL_RATINGS,
    SQL_REVIEWS,
)


def new_movies_news_letter():
    sort_params = "?sort=-created_at&page[size]=51"
    r = requests.get(settings.MOVIE_API_HAND + sort_params)
    result = r.json()
    films_count = len(result)
    films = result[:10]
    send_data = {
        "template_name": "new_film",
        "recipients": "all",
        "template_data": {"films": films, "films_count": films_count},
    }
    requests.post(settings.NOTIFICATION_API_HAND, body=send_data)


def category_per_user_letter():
    client = Client(
        host=settings.CLICKHOUSE_HOST,
        port=settings.CLICKHOUSE_PORT,
        user=settings.CLICKHOUSE_USER,
        password=settings.CLICKHOUSE_PASSWORD,
        secure=True,
        ca_certs=settings.CLICKHOUSE_CERT,
    )
    week_earlier = (datetime.now() - timedelta(days=7)).timestamp()
    client_ids = client.execute(SQL_USER_IDS.format(week_earlier))
    for client_id in client_ids:
        client_id = client_id[0]
        views_films = client.execute(SQL_VIEWS.format(client_id, week_earlier))
        ratings_films = client.execute(SQL_RATINGS.format(client_id, week_earlier))
        reviews_films = client.execute(SQL_REVIEWS.format(client_id, week_earlier))
        films_ids = set([v[0] for v in views_films] + [r[0] for r in ratings_films])
        films = {}
        for film_id in films_ids:
            r = requests.get("http://0.0.0.0:8000/api/v1/film/" + film_id)
            films[film_id] = r.json()["title"]
        send_data = {
            "template_name": "user_activities",
            "recipients": [client_id],
            "template_data": {
                "user_id": client_id,
                "views_films": [films[v[0]] for v in views_films],
                "ratings_films": [films[r[0]] for r in ratings_films],
                "reviews_films": [films[r[0]] for r in reviews_films],
            },
        }
        requests.post(settings.NOTIFICATION_API_HAND, body=send_data)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        logging.info("Added job 'new_movies_news_letter'.")

        """
        scheduler.add_job(
            new_movies_news_letter,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="New movies news letter",
            max_instances=1,
            replace_existing=True,
        )
        """
        scheduler.add_job(
            category_per_user_letter,
            trigger=CronTrigger(
                day_of_week="fri", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="Category per user letter",
            max_instances=1,
            replace_existing=True,
        )
        logging.info("Added weekly job: 'new_movies_news_letter'.")

        try:
            logging.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logging.info("Stopping scheduler...")
            scheduler.shutdown()
            logging.info("Scheduler shut down successfully!")
