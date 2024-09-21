FROM ubuntu:latest
RUN apt-get update && apt-get install -y openssh-client sshpass
RUN mkdir /root/.ssh && ssh-keygen -t rsa -b 2048 -f /root/.ssh/id_rsa -N ""
RUN ssh-keyscan -H $SFTP_HOST >> ~/.ssh/known_hosts
RUN mkdir /script
COPY script.sh /script/puller.sh
COPY converter.sh /script/converter.sh
RUN chmod +x /script/puller.sh
RUN chmod +x /script/converter.sh

ENTRYPOINT ["/script/puller.sh", "/script/converter.sh"]
