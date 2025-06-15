from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Contact, Product


class Command(BaseCommand):
    help = "Add test products and categories to database"

    def handle(self, *args, **options):
        # Удаляем все данные
        Product.objects.all().delete()
        Category.objects.all().delete()
        Contact.objects.all().delete()

        # Загружаем данные из фикстуры
        call_command("loaddata", "catalog_fixture_category.json")
        call_command("loaddata", "catalog_fixture_contacts.json")
        call_command("loaddata", "catalog_fixture_products.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
