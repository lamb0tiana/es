FROM docker.elastic.co/kibana/kibana:8.8.0

# Installer sudo
USER root
RUN apt-get update && apt-get install -y sudo

# Ajouter l'utilisateur elasticsearch au groupe sudo
#RUN usermod -aG sudo elasticsearch

# Réduire l'utilisation de sudo (optionnel)
RUN echo "elasticsearch ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Revenir à l'utilisateur Kibana
USER kibana
