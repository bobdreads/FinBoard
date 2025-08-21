# core/management/commands/create_initial_superuser.py
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Cria um superusuário inicial a partir de variáveis de ambiente.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not all([username, email, password]):
            self.stdout.write(self.style.ERROR(
                'As variáveis de ambiente para o superusuário não estão definidas.'))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(
                f'Superusuário "{username}" já existe.'))
        else:
            User.objects.create_superuser(
                username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(
                f'Superusuário "{username}" criado com sucesso!'))
