from doctest import debug_script

from lib.es.ESclient import ESClient
from lib.constant import riesterAPJMatchingColumns, riesterVNJMatchingColumns, behaviors
from lib.mysql.DBclient import DBclient
from lib.tools import build_criteria
from dotenv import load_dotenv
import os

matched_count_contact = 0
new_count_contact = 0
load_dotenv()
try:
    db = os.getenv('DB_NAME')
    es_host = os.getenv('ES_HOST')
    esClient = ESClient(db, es_host)
    dbClient = DBclient(db)
    query = esClient.queryDocument()
    results = []
    if query.meta.status == 200:
        results = query.body['hits']['hits']
        print('got {} results'.format(len(results)))
        matchingColumns = riesterAPJMatchingColumns + riesterVNJMatchingColumns + riesterVNJMatchingColumns

        for result in results:
            es_id = result['_id']
            source = result['_source']
            es_entries = source.items()
            # if 'user_id' in source : continue
            rows = [{k: item} for k, item in es_entries if item is not None and k in matchingColumns]
            if not rows:
                continue
            first_match = None

            for k, behavior in behaviors:
                criteria = build_criteria(es_entries, behavior)
                match = dbClient.match_string(criteria, es_id)
                first_match = match[0] if match else None

                if first_match:
                    break

            if first_match and 'id' in first_match:
                esClient.updateDocument(es_id, {'user_id': str(first_match['id'])})
                matched_count_contact += 1
            else:
                new_contact_id = dbClient.create_contact(es_entries)
                new_count_contact += 1
                esClient.updateDocument(es_id, {'user_id': new_contact_id})

    print(f'got {matched_count_contact} matches')
    print(f'found {100 * (matched_count_contact / len(results))}% matches with redundant matching')
    print(f'new contact {new_count_contact} || {100 * (new_count_contact / len(results))}% ')
    dbClient.cursor.close()
    dbClient.close_connection()

except Exception as e:
    print(f"Error: {e}")
