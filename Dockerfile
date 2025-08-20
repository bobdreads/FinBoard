# Usar uma imagem base oficial do Python
FROM python:3.12-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Instalar dependências do sistema, se necessário (já temos libpq-dev no passo anterior, mas é bom ter aqui)
# RUN apt-get update && apt-get install -y libpq-dev gcc

# Copiar o arquivo de dependências e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código do projeto para o diretório de trabalho
COPY . .

# Coletar os arquivos estáticos do Django
RUN python manage.py collectstatic --noinput

# Expor a porta que o Gunicorn vai usar
EXPOSE 8000

# Comando para iniciar a aplicação quando o container rodar
# Gunicorn vai servir o arquivo wsgi.py dentro da pasta config
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]