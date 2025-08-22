# Estágio 1: Build do Frontend
FROM node:18-alpine as builder

WORKDIR /app

# Copia os arquivos de configuração do frontend e instala dependências
COPY package*.json ./
COPY tailwind.config.js ./
COPY src/input.css src/
RUN npm install

# Copia o resto do código do frontend
COPY core/templates/core/base.html core/templates/core/base.html
COPY core/static/core/js/main.bundle.js src/

# Roda o comando de build (ajuste se o seu for diferente)
RUN npm run build

# ---

# Estágio 2: Build do Backend Python
FROM python:3.12-slim

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia a aplicação inteira
COPY . .

# Copia os arquivos estáticos construídos do estágio anterior
COPY --from=builder /app/core/static/core/css/output.css /app/core/static/core/css/output.css

# Expõe a porta que o Gunicorn usará
EXPOSE 8000

# Roda o collectstatic
RUN python manage.py collectstatic --noinput

# Define o comando para iniciar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]