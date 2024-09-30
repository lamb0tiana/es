from lib.es.ESclient import ESClient
from lib.constant import riesterAPJMatchingColumns, riesterVNJMatchingColumns, behaviors, QueryBehavior
from lib.mysql.DBclient import DBclient
from lib.tools import build_criteria
from dotenv import load_dotenv
import os

counter_of_matched_contact = {QueryBehavior.ALL_MATCHES: 0, QueryBehavior.ONLY_MAIN_MATCH: 0, QueryBehavior.SOME_MAIN_MATCH: 0,
           QueryBehavior.MAIN_MATCHES_OTHER_MATCHES_ONE: 0}

counter_of_new_contact = {QueryBehavior.ALL_MATCHES: 0, QueryBehavior.ONLY_MAIN_MATCH: 0, QueryBehavior.SOME_MAIN_MATCH: 0,
           QueryBehavior.MAIN_MATCHES_OTHER_MATCHES_ONE: 0}
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

            for behavior in behaviors:

                criteria = build_criteria(es_entries, behavior)
                match = dbClient.match_string(criteria, es_id)
                first_match = match[0] if match else None

                if first_match:
                    break

            if first_match and 'id' in first_match:
                esClient.updateDocument(es_id, {'user_id': str(first_match['id'])})
                matched_count_contact += 1
                counter_of_matched_contact[behavior] += 1
            else:
                new_contact_id = dbClient.create_contact(es_entries)
                new_count_contact += 1
                esClient.updateDocument(es_id, {'user_id': new_contact_id})
                counter_of_new_contact[behavior] += 1


    print(f'GOT {len(results)}  FACTURES')
    print(f'got {matched_count_contact} contact matched || ({100 * (matched_count_contact / len(results)):.2f}%)')
    print(f'got {new_count_contact} new inserted contact || ({100 * (new_count_contact / len(results)):.2f}%)')
    print('DETAILS: ')
    print('FROM ALL MATCHES:: +NOM+PRNOM+EMAIL+TEL')
    print(f'MATCHED CONTACTS {counter_of_matched_contact[behavior.ALL_MATCHES]} || ({100 * (counter_of_matched_contact[behavior.ALL_MATCHES] / len(results)):.2f}%)')
    print(f'NEW CONTACTS {counter_of_new_contact[behavior.ALL_MATCHES]} || ({100 * (counter_of_new_contact[behavior.ALL_MATCHES] / len(results)):.2f}%)')
    print('####################')

    print('FROM ALL MAIN_MATCHES_OTHER_MATCHES_ONE:: +NOM+PRENOM +(EMAIL|TEL)')
    print(f'MATCHED CONTACTS {counter_of_matched_contact[behavior.MAIN_MATCHES_OTHER_MATCHES_ONE]} || ({100 * (counter_of_matched_contact[behavior.MAIN_MATCHES_OTHER_MATCHES_ONE] / len(results)):.2f}%)')
    print(f'NEW CONTACTS {counter_of_new_contact[behavior.MAIN_MATCHES_OTHER_MATCHES_ONE]} || ({100 * (counter_of_new_contact[behavior.MAIN_MATCHES_OTHER_MATCHES_ONE] / len(results)):.2f}%)')
    print('####################')


    print('FROM ALL ONLY_MAIN_MATCH:: +NOM+PRENOM EMAIL TEL')
    print(f'MATCHED CONTACTS {counter_of_matched_contact[behavior.ONLY_MAIN_MATCH]} || ({100 * (counter_of_matched_contact[behavior.ONLY_MAIN_MATCH] / len(results)):.2f}%)')
    print(f'NEW CONTACTS {counter_of_new_contact[behavior.ONLY_MAIN_MATCH]} || ({100 * (counter_of_new_contact[behavior.ONLY_MAIN_MATCH] / len(results)):.2f}%)')
    print('####################')


    print('FROM ALL SOME_MAIN_MATCH:: +(NOM|PRENOM) +(EMAIL|TEL)')
    print(f'NEW CONTACTS {counter_of_matched_contact[behavior.SOME_MAIN_MATCH]} || ({100 * (counter_of_matched_contact[behavior.SOME_MAIN_MATCH] / len(results)):.2f}%)')
    print(f'MATCHED CONTACTS {counter_of_new_contact[behavior.SOME_MAIN_MATCH]} || ({100 * (counter_of_new_contact[behavior.SOME_MAIN_MATCH] / len(results)):.2f}%)')





    dbClient.cursor.close()
    dbClient.close_connection()

except Exception as e:
    print(f"Error: {e}")
