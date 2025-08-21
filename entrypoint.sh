#!/bin/sh

# Executa as migrações do banco de dados
echo "Applying database migrations..."
python manage.py migrate --noinput

# Inicia o processo principal (Gunicorn)
# O "$@" executa o comando que foi passado para o script
exec "$@"