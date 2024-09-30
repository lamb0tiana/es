# Dockerfile
FROM python:3.9-slim

# Installer cron
RUN apt-get update && \
    apt-get install -y cron vim && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY cron /etc/cron.d/cron

RUN chmod 0644 /etc/cron.d/cron

RUN crontab /etc/cron.d/cron
EXPOSE 8000
CMD ["sh", "-c", "cron && fastapi dev --reload --host 0.0.0.0 --port 8000 api/entry.py"]

