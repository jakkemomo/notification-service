from django.conf import settings
from ...models import MailTemplate
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore


import logging


def new_movies_news_letter(template='issue'):
    print("New movies!")


def category_per_user_letter(template='letter'):
    print("Category per users letter!")


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        logging.info("Added job 'new_movies_news_letter'.")

        scheduler.add_job(
            new_movies_news_letter,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="New movies news letter",
            max_instances=1,
            replace_existing=True,
        )
        scheduler.add_job(
            category_per_user_letter,
            trigger=CronTrigger(
                day_of_week="fri", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="Category per user letter",
            max_instances=1,
            replace_existing=True,
        )
        logging.info(
            "Added weekly job: 'new_movies_news_letter'."
        )

        try:
            logging.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logging.info("Stopping scheduler...")
            scheduler.shutdown()
            logging.info("Scheduler shut down successfully!")
