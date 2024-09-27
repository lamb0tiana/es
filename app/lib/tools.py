from lib.constant import riesterDBColumns, riesterAPJMatchingColumns, riesterVNJMatchingColumns, requiredMatchingFields, \
    QueryBehavior, mappingDbFields
import re
import itertools


def sanitize_string(string):
    pattern = r'\+33|-'
    string = re.sub(pattern, '', string)
    return re.sub(r'\+', ' ', string)


def generate_matching_query(search_terms: str):
    query = f"""
    SELECT
        MATCH({', '.join(riesterDBColumns)}) AGAINST('{search_terms}') AS score,
        l.*
    FROM
        lms_contact l
    WHERE
        MATCH({', '.join(riesterDBColumns)}) AGAINST('{search_terms}' IN BOOLEAN MODE)
    ORDER BY
        1 DESC;
    """
    return query


def build_criteria(criterias: list, behavior: QueryBehavior = QueryBehavior.ALL_MATCHES):
    matchingColumns = riesterAPJMatchingColumns + riesterVNJMatchingColumns + riesterVNJMatchingColumns
    # all required fields (nom + prenom)
    main_field_candidates = {k: sanitize_string(v) for k, v in criterias if
                             v is not None and k in matchingColumns and k in requiredMatchingFields}
    # all unecessary fields (email+phone)
    pass_field_candidates = {
        k: f'"{sanitize_string(v)}"' if re.search(r'email', k, re.IGNORECASE) else sanitize_string(v) for k, v in
        criterias if
        v is not None and k in matchingColumns and k not in requiredMatchingFields}

    is_main_matching_query = behavior in [QueryBehavior.ALL_MATCHES, QueryBehavior.ONLY_MAIN_MATCH]
    is_main_and_one_right = behavior ==  QueryBehavior.MAIN_MATCHES_OTHER_MATCHES_ONE
    required_fields_candidates = [
        "+" + item if is_main_matching_query or is_main_and_one_right else item for item in
        main_field_candidates.values()]

    pass_fields_candidates = ["+" + item if behavior == QueryBehavior.ALL_MATCHES else item for item in
                              pass_field_candidates.values()]

    separator = ' ' if is_main_matching_query or is_main_and_one_right  else '|'
    required_string = separator.join(set(required_fields_candidates))
    pass_string = ('|' if is_main_and_one_right else separator).join(set(pass_fields_candidates))

    if is_main_and_one_right:
        criteria = "({main})+({right})".format( main=required_string, right=pass_string)
    else:
        criteria = required_string + ' ' + pass_string if is_main_matching_query else "+({})+({})".format(
            required_string,
            pass_string)
    return criteria


def find_key(search_key, candidates):
    return list({k: v for k, v in candidates if search_key in v}.keys())


def build_insert_query(rows: list):
    cols = []
    values = []
    for row_item in rows:
        value = str(row_item[1]).strip()
        _key = find_key(row_item[0], mappingDbFields.items())
        if value is None or value == '' or len(_key) == 0: continue
        cols.append(_key[0].strip())
        values.append(re.sub(r'\+33|-', '0', value.strip()))
    if len(cols) == len(values):
        cols = "{}".format(",".join(cols))
        values = "'{}'".format("','".join(values))
        return "INSERT INTO lms_contact ({cols}) VALUES ({values})".format(cols=cols, values=values)

    return None


def extract_insertable_field_data(es_entries: list):
    dbFields = mappingDbFields.values()
    fields = set(list(itertools.chain.from_iterable([item for item in dbFields])))
    return [[k, item] for k, item in es_entries if item is not None and k in fields]
