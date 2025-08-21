# core/management/commands/set_admin_password.py
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Define a senha para um superusuário especificado por variáveis de ambiente.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write(self.style.ERROR(
                'As variáveis DJANGO_SUPERUSER_USERNAME e DJANGO_SUPERUSER_PASSWORD devem ser definidas.'))
            return

        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(
                f'Senha para o usuário "{username}" foi definida com sucesso!'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f'Usuário "{username}" não encontrado.'))
