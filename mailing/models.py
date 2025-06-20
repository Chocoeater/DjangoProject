from smtplib import SMTPException

from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.db import models
from django.utils import timezone

# Create your models here.


class Recipient(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name="Адрес электронной почты",
        help_text="Введите адрес электронной почты получателя.",
    )
    full_name = models.CharField(
        max_length=200,
        verbose_name="Ф.И.О.",
        help_text="Введите фамилию, имя и отчество (при наличии) получателя.",
    )
    comment = models.TextField(
        verbose_name="Комментарий",
        help_text="Введите комментарий к профилю получателя (не обязательно).",
        null=True,
        blank=True,
    )


class Message(models.Model):
    subject = models.CharField(
        max_length=200, verbose_name="Тема письма", help_text="Введите тему письма"
    )
    body = models.TextField(verbose_name="Тест письма", help_text="Введите текст письма")
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='messages', verbose_name='Владелец')


class Mailing(models.Model):
    STATUS_CHOICES = [
        ("created", "Cоздана"),
        ("started", "Запущена"),
        ("ended", "Завершена"),
    ]
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='mailings', verbose_name='Владелец')
    start_time = models.DateTimeField(verbose_name="Время начала")
    end_time = models.DateTimeField(verbose_name="Время окончания")
    status = models.CharField(
        choices=STATUS_CHOICES, default="created", verbose_name="Статус рассылки"
    )
    message = models.ForeignKey(
        "Message", on_delete=models.CASCADE, verbose_name="Сообщение"
    )
    recipient = models.ManyToManyField("Recipient", verbose_name="Получатели")

    def update_status(self):
        now = timezone.now()
        if self.start_time <= now <= self.end_time:
            self.status = "started"
        elif now > self.end_time:
            self.status = "ended"
        else:
            self.status = "created"

    # Для автоматического обновления статуса
    def save(self, *args, **kwargs):
        self.update_status()
        super().save(*args, **kwargs)

    def send(self):
        connection = get_connection()
        for rec in self.recipient.all():
            email = EmailMessage(
                subject=self.message.subject,
                body=self.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[rec.email],
                connection=connection,
            )

        try:
            email.send()
            Attempt.objects.create(
                mailing=self,
                status="success",
                answer_post_server="Письмо успешно отправлено",
            )
        except SMTPException as e:
            Attempt.objects.create(
                mailing=self, status="fail", answer_post_server=str(e)
            )
        except Exception as e:
            Attempt.objects.create(
                mailing=self, status="fail", answer_post_server=str(e)
            )


class Attempt(models.Model):
    status_choice = [("success", "Успешно"), ("fail", "Не успешно")]

    created_at = models.DateTimeField(auto_now=True, verbose_name="Время попытки")
    status = models.CharField(choices=status_choice, verbose_name="Статус попытки")
    answer_post_server = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(
        "Mailing", verbose_name="Рассылка", on_delete=models.CASCADE
    )
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='attempts', verbose_name='Владелец')
