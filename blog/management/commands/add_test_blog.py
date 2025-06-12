from django.core.management import call_command
from django.core.management.base import BaseCommand

from blog.models import BlogRecord


class Command(BaseCommand):
    help = "Add test products and categories to database"

    def handle(self, *args, **options):
        # Удаляем все данные
        BlogRecord.objects.all().delete()

        # Загружаем данные из фикстуры
        call_command("loaddata", "blog_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
