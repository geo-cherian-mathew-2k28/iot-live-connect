FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
# Koyeb handles the port automatically via the PORT env var
CMD sh -c "gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT app:app"
