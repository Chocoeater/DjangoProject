from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создает пользователя с правами кастомного модератора"

    def handle(self, *args, **options):
        user = User.objects.create(email="moderator@mail.ru", country="ru")
        user.set_password("1234qwer")
        user.is_active = True
        user.save()

        group = Group.objects.get(name="Модераторы")
        user.groups.add(group)

        self.stdout.write(self.style.SUCCESS("Модератор создан!"))
