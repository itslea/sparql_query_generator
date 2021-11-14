import requests


def fetch_data(triples):
    """Fetches data from SPAQRL endpoint."""

    # Create query for SPARQL endpoint
    fetch_query = 'SELECT DISTINCT * FROM <http://dbpedia.org> WHERE { '
    filter_string = 'FILTER('
    counter = 2

    for i in range(1, triples + 1):
        fetch_query += '?s ?p' + str(i) + ' ?o' + str(i) + ' . '
        for j in range(counter, triples + 1):
            filter_string += '?p' + str(i) + ' != ?p' + str(j)
            if (i != triples - 1 and j != triples + 1):
                filter_string += ' && '
        counter += 1

    filter_string += ')'
    fetch_query += filter_string + ' FILTER(1 > <SHORT_OR_LONG::bif:rnd> (10000, ?s)) } LIMIT 1'  # TODO: takes too long to process ' } ORDER BY RAND() LIMIT 1', choose random answer

    print(fetch_query)
    result = requests.get('http://localhost:8890/sparql', params={'format': 'json', 'query': fetch_query})
    return result.json()


def generate_query(queries, triples, operator_prob, var_prob):
    """Generates query."""

    query = ''
    
    endpoint_data = fetch_data(triples)
    return(endpoint_data)

