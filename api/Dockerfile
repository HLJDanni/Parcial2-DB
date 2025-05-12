# Versión simplificada sin wait-for-it
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar netcat (opcional, si aún lo necesitas para otras cosas)
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY . .

# Comando directo sin wait-for-it
CMD ["sh", "-c", "python replicador.py && flask run --host=0.0.0.0"]