FROM ubuntu:latest

RUN apt-get update && apt-get install -y openssh-client sshpass cron vim
RUN mkdir -p /root/.ssh && ssh-keygen -t rsa -b 2048 -f /root/.ssh/id_rsa -N ""
RUN mkdir /script
COPY .env script.sh /script/
RUN (cat /script/.env && echo "" && cat /script/script.sh) > /script/puller.sh
RUN chmod +x /script/puller.sh

COPY csv_puller /etc/cron.d/csv_puller
RUN chmod 0644 /etc/cron.d/csv_puller
RUN crontab /etc/cron.d/csv_puller

CMD /bin/bash /script/puller.sh & cron -f