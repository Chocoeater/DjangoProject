from smtplib import SMTPException

from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.db import models
from django.utils import timezone

# Create your models here.


class Recipient(models.Model):
    class Meta:
        verbose_name = 'Получатель-клиент'
        verbose_name_plural = 'Получатели-клиенты'

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
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='recipients', verbose_name='Владелец')


class Message(models.Model):
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    subject = models.CharField(
        max_length=200, verbose_name="Тема письма", help_text="Введите тему письма"
    )
    body = models.TextField(verbose_name="Тест письма", help_text="Введите текст письма")
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='messages', verbose_name='Владелец')


class Mailing(models.Model):
    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ('can_blocked', 'Может блокировать'),
        ]

    STATUS_CHOICES = [
        ("created", "Cоздана"),
        ("started", "Запущена"),
        ("ended", "Завершена"),
        ("stopped", "Остановлена вручную"),
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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')


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
                    owner=self.owner
                )
            except SMTPException as e:
                Attempt.objects.create(
                    mailing=self, status="fail", answer_post_server=str(e), owner=self.owner
                )
            except Exception as e:
                Attempt.objects.create(
                    mailing=self, status="fail", answer_post_server=str(e), owner=self.owner
                )


class Attempt(models.Model):
    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'

    status_choice = [("success", "Успешно"), ("fail", "Не успешно")]

    created_at = models.DateTimeField(auto_now=True, verbose_name="Время попытки")
    status = models.CharField(choices=status_choice, verbose_name="Статус попытки")
    answer_post_server = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(
        "Mailing", verbose_name="Рассылка", on_delete=models.CASCADE
    )
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='attempts', verbose_name='Владелец')

