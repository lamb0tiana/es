#!/bin/bash

# Créer le répertoire .ssh s'il n'existe pas et s'assurer des bonnes permissions
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "go to $SFTP_HOST"
# Ajouter la clé d'hôte SFTP au fichier known_hosts
ssh-keyscan -H "$SFTP_HOST" >> ~/.ssh/known_hosts
chmod 644 ~/.ssh/known_hosts
if [ -d "$LOCAL_DIR/riester" ]; then
  echo "Suppression du contenu du répertoire $LOCAL_DIR/riester"
  rm -rf "$LOCAL_DIR/riester"/*
else
  echo "Le répertoire $LOCAL_DIR/riester n'existe pas. on passe"
fi
echo "pulling csv...."
#
## Connexion SFTP avec sshpass
sshpass -p "$SFTP_PASSWORD" sftp -o StrictHostKeyChecking=no $SFTP_USER@$SFTP_HOST <<EOF
cd $REMOTE_DIR
lcd $TEMP_DIR
mget *.csv
bye
EOF
echo "Fichiers récupérés dans $TEMP_DIR :"

echo "handle csv"
if ls "$TEMP_DIR"/*.csv 1> /dev/null 2>&1; then
  echo "conversion des fichiers en séparateur à virgules :"

  for file in "$TEMP_DIR"/*.csv; do
    if [ -f "$file" ]; then
      echo "Traitement du fichier : $file \n"
      echo "FIX ENCODING"
      iconv -f ISO-8859-1 -t UTF-8 $file -o $file
      echo "Suppression de la première ligne"
      sed -i '1d' "$file"
      # Remplacer le séparateur de tabulation par des virgules directement dans le fichier original
      sed -i 's/\t/,/g' "$file"
      echo "Fichier converti et remplacé : $file"
    fi
  done
else
  echo "Aucun fichier CSV trouvé dans $TEMP_DIR"
fi
mv $TEMP_DIR/* $LOCAL_DIR/riester/