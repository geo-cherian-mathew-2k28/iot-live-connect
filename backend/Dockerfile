FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
# Koyeb uses PORT env var, which we handle in app.py
EXPOSE 5000

CMD ["python", "app.py"]
