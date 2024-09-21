#!/bin/bash
LOCAL_DIR="../data/riester"
if ls "$LOCAL_DIR"/*.csv 1> /dev/null 2>&1; then
  echo "conversion des fichiers en séparateur à virgules :"

  for file in "$LOCAL_DIR"/*.csv; do
    if [ -f "$file" ]; then
      echo "Traitement du fichier : $file \n"
      echo "Suppression de la première ligne"
      sed -i '1d' "$file"
      # Remplacer le séparateur de tabulation par des virgules directement dans le fichier original
      sed -i 's/\t/,/g' "$file"
      echo "Fichier converti et remplacé : $file"
    fi
  done
else
  echo "Aucun fichier CSV trouvé dans $LOCAL_DIR"
fi
