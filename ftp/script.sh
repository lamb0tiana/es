#!/bin/bash

# Créer le répertoire .ssh s'il n'existe pas et s'assurer des bonnes permissions
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Ajouter la clé d'hôte SFTP au fichier known_hosts
ssh-keyscan -H "$SFTP_HOST" >> ~/.ssh/known_hosts
chmod 644 ~/.ssh/known_hosts

echo "pulling csv...."

# Connexion SFTP avec sshpass
sshpass -p "$SFTP_PASSWORD" sftp -o StrictHostKeyChecking=no $SFTP_USER@$SFTP_HOST <<EOF
cd $REMOTE_DIR
lcd $LOCAL_DIR
mget *.csv
bye
EOF
