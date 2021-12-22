import random
import requests

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
    fetch_query += filter_string + ' FILTER(1 > <SHORT_OR_LONG::bif:rnd> (10000, ?s)) } LIMIT 1'  # TODO: takes too long to process ' } ORDER BY RAND() LIMIT 1', choose random answer

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


def create_union_string(union_patterns):
    union_str = "{ "
    part1_len = random.randint(1, len(union_patterns) - 1)

    for i in range(0, part1_len):
        union_str += union_patterns[i] + " "
    union_str += "} UNION { "
    for i in range(part1_len, len(union_patterns)):
        union_str += union_patterns[i] + " "
    union_str += "} "

    return union_str


def create_optional_string(optional_patterns):
    optional_str = "OPTIONAL { "
    for elem in optional_patterns:
        optional_str += elem + " "
    optional_str += "} "

    return optional_str


def create_shape_string(rest_patterns):
    rest_str = ""
    for elem in rest_patterns:
        rest_str += elem + " "

    return rest_str


def create_operators(triples, operator_prob):
    """Creates the operators."""
    where_str = "WHERE { "
    bool_distinct = False
    bool_optional = False
    bool_union = False

    if triples >= 3:
        if random.random() <= operator_prob: bool_distinct = True
        if random.random() <= operator_prob: bool_optional = True
        if random.random() <= operator_prob: bool_union = True
    else:
        if triples == 2:
            if random.random() <= operator_prob: bool_distinct = True
            if random.random() <= operator_prob: bool_union = True
        elif triples == 1:
            if random.random() <= operator_prob: bool_distinct = True
            if random.random() <= operator_prob: bool_optional = True
    
    if bool_distinct:
        print("TODO")

    if bool_optional and bool_union:
        print("HIERRRRR")
        chooseFirst = ["optional", "union"]
        first = random.choices(chooseFirst)

        first[0] == "optional"
        # Divide patterns durch 3 -> optional, union, rest
        if first[0] == "optional":
            o = random.randint(1, triples - 2)
            u = random.randint(2, triples - o)
            r = triples - o - u

            rest_patterns = []
            for i in range(0, r):
                rest_patterns.append(patterns[i])
            print("rest " + str(r) + " :")
            print(rest_patterns)

            optional_patterns = []
            for i in range(r, r + o):
                optional_patterns.append(patterns[i])
            print("optional " + str(o) + " :")
            print(optional_patterns)

            union_patterns = []
            for i in range(r + o, triples):
                union_patterns.append(patterns[i])
            print("union " + str(u) + " :")
            print(union_patterns)

            where_str += create_shape_string(rest_patterns) + create_optional_string(optional_patterns) + create_union_string(union_patterns)
        else:
            u = random.randint(2, triples - 1)
            o = random.randint(1, triples - u)
            r = triples - o - u

            rest_patterns = []
            for i in range(0, r):
                rest_patterns.append(patterns[i])
            print("rest " + str(r) + " :")
            print(rest_patterns)

            union_patterns = []
            for i in range(r, r + u):
                union_patterns.append(patterns[i])
            print("union " + str(u) + " :")
            print(union_patterns)

            optional_patterns = []
            for i in range(r + u, triples):
                optional_patterns.append(patterns[i])
            print("optional " + str(o) + " :")
            print(optional_patterns)

            where_str += create_shape_string(rest_patterns) + create_union_string(union_patterns) + create_optional_string(optional_patterns)

    elif bool_optional:
        o = random.randint(1, triples)
        r = triples - o

        rest_patterns = []
        for i in range(0, r):
            rest_patterns.append(patterns[i])

        optional_patterns = []
        for i in range(r, triples):
            optional_patterns.append(patterns[i])

        where_str += create_shape_string(rest_patterns) + create_optional_string(optional_patterns)

    elif bool_union:
        u = random.randint(2, triples)
        r = triples - u

        rest_patterns = []
        for i in range(0, r):
            rest_patterns.append(patterns[i])

        union_patterns = []
        for i in range(r, triples):
            union_patterns.append(patterns[i])

        where_str += create_shape_string(rest_patterns) + create_union_string(union_patterns)

    where_str += "}"
    return where_str


def generate_query(queries, triples, operator_prob, var_prob):
    """Generates query."""
    query = ''
    endpoint_data = fetch_data(triples)
    query_shape = create_query_shape(endpoint_data, triples, var_prob)
    print(query_shape)

    return endpoint_data
