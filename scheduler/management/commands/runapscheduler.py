import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.core.management import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
import logging
from mailing.jobs import send_scheduler_mailings

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    logger.info("Запускается планировщик...")
    help = 'Запуск планировщика задач'

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler(timezone='Europe/Moscow') # Фоновый планировщик
        scheduler.add_jobstore(DjangoJobStore(), 'default') # Django-хранилище для задач

        scheduler.add_job(
            send_scheduler_mailings,
            trigger=IntervalTrigger(minutes=1),
            id='send_mailings',
            max_instances=2,
            replace_existing=True,
        )
        logger.info("Планировщик настроен, запускается...")
        scheduler.start()
        try:
            while True:
                time.sleep(5)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()


