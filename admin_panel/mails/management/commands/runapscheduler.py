import logging
from datetime import datetime, timedelta

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore, logger

from admin_panel.mails.sql_queries import (
    SQL_RATINGS,
    SQL_REVIEWS,
    SQL_USER_IDS,
    SQL_VIEWS,
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


def get_data_from_clickhouse(query: str) -> str:
    url = f"https://{settings.CLICKHOUSE_HOST}:{settings.CLICKHOUSE_PORT}/?database={settings.CLICKHOUSE_DB}&query={query}"
    auth = {
        "X-ClickHouse-User": settings.CLICKHOUSE_USER,
        "X-ClickHouse-Key": settings.CLICKHOUSE_PASSWORD,
    }
    try:
        res = requests.get(url, headers=auth, verify=settings.CLICKHOUSE_CERT)
        res.raise_for_status()
        return res.text
    except Exception as e:
        logger.error("Error while sending request to Clickhouse Storage: %s" % e)
        return "\n"


def get_list_of_clickhouse_records(query: str) -> list:
    clickhouse_data = get_data_from_clickhouse(query)
    return list(set(filter(None, clickhouse_data.split("\n"))))


def category_per_user_letter():
    week_earlier = (datetime.now() - timedelta(days=7)).timestamp()
    client_ids = get_list_of_clickhouse_records(SQL_USER_IDS.format(week_earlier))
    for client_id in client_ids:
        error = False
        views_films = get_list_of_clickhouse_records(
            SQL_VIEWS.format(client_id, week_earlier)
        )
        ratings_films = get_list_of_clickhouse_records(
            SQL_RATINGS.format(client_id, week_earlier)
        )
        reviews_films = get_list_of_clickhouse_records(
            SQL_REVIEWS.format(client_id, week_earlier)
        )
        films_ids = set(views_films + ratings_films + reviews_films)
        films = {}
        for film_id in films_ids:
            try:
                r = requests.get(
                    f"{settings.MOVIE_API_HAND}/v1/film/{film_id}",
                    headers={"Authorization": "ADMIN"},
                )
                films[film_id] = r.json()["title"]
            except Exception as e:
                logger.error("Error while sending request to Movie API: %s" % e)
                error = True
                continue
        if not error and films_ids:
            payload = {
                "delivery_type": "email",
                "content_type": "news",
                "message": {
                    "recipients": [client_id],
                    "template_name": "user_activities",
                    "template_data": {
                        "views_films": [films[film_id] for film_id in views_films],
                        "ratings_films": [films[film_id] for film_id in ratings_films],
                        "reviews_films": [films[film_id] for film_id in reviews_films],
                    },
                },
            }
            try:
                requests.post(
                    f"{settings.NOTIFICATION_API_HAND}/notification", json=payload
                )
            except Exception as e:
                logger.error("Error while sending request to Notification API: %s" % e)


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
                day_of_week="mon", hour="23", minute="58", second="35"
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
