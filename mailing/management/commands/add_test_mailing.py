from click import BaseCommand


class Command(BaseCommand):
    help = 'Создание тестовой рассылки'

    def handle(self, *args, **kwargs):
