FROM python:3.11-slim

WORKDIR /app

# Copy requirements from the backend folder
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . .

# Change working directory to the backend folder
WORKDIR /app/backend

ENV PYTHONUNBUFFERED=1

# Run gunicorn from the backend directory
CMD gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT app:app
