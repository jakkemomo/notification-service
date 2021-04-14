from django.conf import settings
from .models import MailTemplate
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore

from ..config.settings.base import RABBIT_HOST, RABBIT_QUEUE

import logging
import pika


def send_mail(template='issue'):
    template_object = MailTemplate.objects.get(name=template)
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RABBIT_QUEUE)
    channel.basic_publish(exchange='',
                          routing_key=RABBIT_QUEUE,
                          body=template_object.body.encode('utf-8'))
    connection.close()


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        logging.info("Added job 'send_mail'.")

        scheduler.add_job(
            send_mail,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="send_mail",
            max_instances=1,
            replace_existing=True,
        )
        logging.info(
            "Added weekly job: 'send_mail'."
        )

        try:
            logging.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logging.info("Stopping scheduler...")
            scheduler.shutdown()
            logging.info("Scheduler shut down successfully!")
