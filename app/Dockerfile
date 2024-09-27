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
#COPY crontab /etc/cron.d/my_cron

RUN #chmod 0644 /etc/cron.d/my_cron

RUN #crontab /etc/cron.d/my_cron

CMD ["cron", "-f"]
