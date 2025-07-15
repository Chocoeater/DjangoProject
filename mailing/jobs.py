import logging

from django.utils.timezone import now

from mailing.models import Mailing

logger = logging.getLogger(__name__)


def send_scheduler_mailings():
    logger.info(f"[ЗАДАЧА] Рассылка пошла! {now()}")
    current_time = now()
    logger.info(f"[scheduler] Проверка рассылок на {current_time}")
    mailings_to_start = Mailing.objects.filter(
        status="created", start_time__lte=current_time, end_time__gt=current_time
    )

    for mailing in mailings_to_start:
        logger.info(f"[scheduler] Запуск рассылки ID={mailing.id}")
        mailing.send()
        mailing.status = "started"
        mailing.save()

    Mailing.objects.filter(status="started", end_time__lte=current_time).update(
        status="ended"
    )
