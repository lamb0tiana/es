#!/bin/bash

setup_ssh() {
  mkdir -p ~/.ssh
  chmod 700 ~/.ssh
  echo "Go to $SFTP_HOST"
  ssh-keyscan -H "$SFTP_HOST" >> ~/.ssh/known_hosts
  chmod 644 ~/.ssh/known_hosts
}

manage_directory() {
  mkdir -p "$LOCAL_DIR/riester"
  rm -rf "$LOCAL_DIR/riester"/* # clean last files
  mkdir -p "$TEMP_DIR"
}

pull_csv_files() {
  echo "Pulling CSV..."
  sshpass -p "$SFTP_PASSWORD" sftp -o StrictHostKeyChecking=no "$SFTP_USER@$SFTP_HOST" <<EOF
cd $REMOTE_DIR
lcd $TEMP_DIR
mget *.csv
bye
EOF
  echo "Fichiers récupérés dans $TEMP_DIR :"
}

process_csv_files() {
  echo "Handle CSV"
  if ls "$TEMP_DIR"/*.csv 1> /dev/null 2>&1; then
    echo "Convert csv seprator to comma"
    for file in "$TEMP_DIR"/*.csv; do
      if [ -f "$file" ]; then
        echo "FIX ENCODING"
        iconv -f ISO-8859-1 -t UTF-8 "$file" -o "$file"
        echo "REMOVE UNNECESSARY FIRST LINE"
        sed -i '1d' "$file"
        sed -i 's/\t/,/g' "$file"
        echo "handled file > : $file"
      fi
    done
  else
    echo "no file found to $TEMP_DIR"
  fi
}

move_processed_files() {
  mkdir -p "$LOCAL_DIR/riester/"
  mv "$TEMP_DIR"/* "$LOCAL_DIR/riester/"
}

setup_ssh
manage_directory
pull_csv_files
process_csv_files
move_processed_files
