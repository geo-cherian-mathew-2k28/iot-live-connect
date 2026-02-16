FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
# Professional Koyeb Config: Bind to the dynamic PORT provided by the platform
CMD gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT app:app
