# Usar uma imagem base oficial do Python
FROM python:3.12-slim

# Definir variáveis de ambiente
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1

# Definir o diretório de trabalho dentro do container
#WORKDIR /app

# Copiar o arquivo de dependências e instalar
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código do projeto para o diretório de trabalho
#COPY . .

# Dar permissão de execução para o script de inicialização
#RUN chmod +x /app/entrypoint.sh

# Coletar os arquivos estáticos do Django
#RUN python manage.py collectstatic --noinput

# <<< ADIÇÃO IMPORTANTE >>>
# Rodar as migrações do banco de dados automaticamente
# RUN python manage.py migrate --noinput

# Criar o superusuário inicial se ele não existir
#RUN python manage.py create_initial_superuser
#RUN python manage.py set_admin_password

# Expor a porta que o Gunicorn vai usar
#EXPOSE 8000

# Comando para iniciar a aplicação quando o container rodar
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
CMD ["sh", "-c", "echo '>>>> INÍCIO DO TESTE DE VARIÁVEL <<<<' && echo 'A DATABASE_URL que o container está recebendo é:' && echo $DATABASE_URL && echo '>>>> FIM DO TESTE DE VARIÁVEL <<<<' && sleep 3600"]
# Cache buster v4