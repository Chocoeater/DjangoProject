from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Add test products and categories to database"

    def handle(self, *args, **options):
        # Удаляем все данные
        User.objects.all().delete()
        Group.objects.all().delete()

        # Загружаем данные из фикстуры
        call_command("loaddata", "groups_fixture.json")
        call_command("loaddata", "users_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
