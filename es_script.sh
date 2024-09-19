#!/bin/bash

# Wait for Elasticsearch to be ready
until curl -u elastic:$ELASTIC_PASSWORD -k --fail https://localhost:9200/_cluster/health; do
  echo "Waiting for Elasticsearch to start..."
  sleep 5
done

# Create the kibana_system_user
echo "Creating kibana_system_user..."
curl -u elastic:$ELASTIC_PASSWORD -X POST "https://localhost:9200/_security/user/kibana_system_user" -H 'Content-Type: application/json' -d'
{
  "password": "'"$KIBANA_PASSWORD"'",
  "roles": ["kibana_system"],
  "full_name": "Kibana System User",
  "email": "kibana_system_user@example.com"
}'
