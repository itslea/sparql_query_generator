import random
import requests
import operator_handler as oh

patterns = ["?s1 ?p1 ?o1 .", "?s1 ?p2 ?o2 .", "?s1 ?p3 ?o3 .", "?s1 ?p4 ?o4 ."]  # patterns is a list of strings containing the triple patterns with size = n


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
    fetch_query += filter_string + ' FILTER(1 > <SHORT_OR_LONG::bif:rnd> (10000, ?s)) } LIMIT 1'

    # print(fetch_query)
    result = requests.get('https://dbpedia.org/sparql', params={'format': 'json', 'query': fetch_query})
    return result.json()


def create_query_shape(endpoint_data, triples, var_prob):
    """Creates the basic shape of the query while replacing constants with
    variables according to the variable probability"""

    endpoint_data = endpoint_data['results']['bindings'][0]
    # print(endpoint_data)

    query_shape = ''
    pred_var_counter = 1
    obj_var_counter = 1

    subject = endpoint_data['s']
    if random.random() <= var_prob:
        subject = '?s'
    else:
        if subject['type'] == 'uri':
            subject = '<' + subject['value'] + '>'
        # elif(subject['type' == ]) blank node

    for i in range(1, triples + 1):
        predicate = endpoint_data['p' + str(i)]
        objectt = endpoint_data['o' + str(i)]

        if random.random() <= var_prob:
            predicate = '?p' + str(pred_var_counter)
            pred_var_counter += 1
        else:
            predicate = '<' + predicate['value'] + '>'

        if random.random() <= var_prob:
            objectt = '?o' + str(obj_var_counter)
            obj_var_counter += 1
        else:
            if objectt['type'] == 'uri':
                objectt = '<' + objectt['value'] + '>'
            elif objectt['type'] == 'literal':
                objectt = '\"' + objectt['value'] + '\"'
            # elif blank node

        query_shape += subject + ' ' + predicate + ' ' + objectt + ' . '

    return query_shape


def generate_query(queries, triples, operator_prob, var_prob):
    """Generates query."""
    query = ''
    endpoint_data = fetch_data(triples)
    query_shape = create_query_shape(endpoint_data, triples, var_prob)
    print(query_shape)

    #  Use fetch query
    #  generate triples and put them in a []
    #  call operator handler and receive WHERE part
    #  create entire query: distinct, choose variables to put in SELECT, add FROM and then the WHERE

    return endpoint_data
