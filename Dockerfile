FROM python:3.11-slim

WORKDIR /app

# Copy requirements from the backend folder
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . .

ENV PYTHONUNBUFFERED=1

# Command to run from the root, pointing to the app inside the backend folder
CMD gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT backend.app:app
