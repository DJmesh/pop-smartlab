# Python com patch (Render exige MAJOR.MINOR.PATCH)
FROM python:3.12.1-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Dependências de sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Código
COPY . .

# Coleta estáticos no build (usa SQLite fallback se DATABASE_URL não existir no build)
RUN python manage.py collectstatic --noinput

# Entrypoint (migrações + gunicorn)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
CMD ["/entrypoint.sh"]
