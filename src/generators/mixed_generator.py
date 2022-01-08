import random
from timeit import default_timer as timer
import helpers.data_handler as dh
import helpers.operator_handler as oh


def create_triple_patterns(endpoint_data_first, endpoint_data_second, var_prob, connection):
    """Creates the basic shape of the query while replacing constants with
    variables according to the variable probability"""

    subj_var_counter = 1
    pred_var_counter = 1
    obj_var_counter = 1
    patterns = []
    variables = []

    con_var = "?connect"
    con_is_var = random.random() <= var_prob
    print("Con is var: ", con_is_var)

    if endpoint_data_first['shape'] == "star_subject":
        patterns_and_var = create_triple_patterns_subject(endpoint_data_first['patterns'], var_prob, connection, con_is_var, con_var, pred_var_counter, obj_var_counter)
        pred_var_counter = patterns_and_var['pred_counter']
        obj_var_counter = patterns_and_var['obj_counter']
    elif endpoint_data_first['shape'] == "star_object":
        patterns_and_var = create_triple_patterns_object(endpoint_data_first['patterns'], var_prob, connection, con_is_var, con_var, pred_var_counter, subj_var_counter)
        subj_var_counter = patterns_and_var['subj_counter']
        pred_var_counter = patterns_and_var['pred_counter']
    elif endpoint_data_first['shape'] == "path":
        patterns_and_var = create_triple_patterns_path(endpoint_data_first['patterns'], var_prob, connection, con_is_var, con_var, pred_var_counter, obj_var_counter)
        pred_var_counter = patterns_and_var['pred_counter']
        obj_var_counter = patterns_and_var['obj_counter']

    patterns += patterns_and_var['patterns']
    variables += patterns_and_var['variables']

    patterns_and_var2 = []

    if endpoint_data_second['shape'] == "star_subject":
        patterns_and_var2 = create_triple_patterns_subject(endpoint_data_second['patterns'], var_prob, connection, con_is_var, con_var, pred_var_counter, obj_var_counter)
    elif endpoint_data_second['shape'] == "star_object":
        patterns_and_var2 = create_triple_patterns_object(endpoint_data_second['patterns'], var_prob, connection, con_is_var, con_var, pred_var_counter, subj_var_counter)
    elif endpoint_data_second['shape'] == "path":
        patterns_and_var2 = create_triple_patterns_path(endpoint_data_second['patterns'], var_prob, connection, con_is_var, con_var, pred_var_counter, obj_var_counter)

    patterns += patterns_and_var2['patterns']
    variables += patterns_and_var2['variables']

    # print("CREATE_TRIPLE_PATTERNS:  ", patterns)
    return {"patterns": patterns, "variables": variables}


def create_triple_patterns_subject(endpoint_data, var_prob, connection, con_is_var, con_var, pred_var_counter, obj_var_counter):
    """Creates the basic shape of the query while replacing constants with
    variables according to the variable probability"""

    patterns = []
    variables = []

    subject = endpoint_data[0]['s']
    if subject == connection:
        if con_is_var:
            subject = con_var
            variables.append(subject)
        else:
            if subject['type'] == 'uri':
                subject = '<' + subject['value'] + '>'
    else:
        if random.random() <= var_prob:
            subject = '?s'
            variables.append(subject)
        else:
            if subject['type'] == 'uri':
                subject = '<' + subject['value'] + '>'

    for elem in endpoint_data:
        predicate = elem['p']
        objectt = elem['o']

        if random.random() <= var_prob:
            predicate = '?p' + str(pred_var_counter)
            variables.append(predicate)
            pred_var_counter += 1
        else:
            predicate = '<' + predicate['value'] + '>'

        if elem['o'] == connection:
            if con_is_var:
                objectt = con_var
                variables.append(objectt)
            else:
                objectt = dh.DataHandler().get_object_string(objectt)
        else:
            if random.random() <= var_prob:
                objectt = '?o' + str(obj_var_counter)
                variables.append(objectt)
                obj_var_counter += 1
            else:
                objectt = dh.DataHandler().get_object_string(objectt)

        patterns.append(subject + ' ' + predicate + ' ' + objectt + ' .')

    return {"patterns": patterns, "variables": variables, "pred_counter": pred_var_counter, "obj_counter": obj_var_counter}


def create_triple_patterns_object(endpoint_data, var_prob, connection, con_is_var, con_var, pred_var_counter, subj_var_counter):
    """Creates the basic shape of the query while replacing constants with
    variables according to the variable probability"""

    patterns = []
    variables = []

    objectt = endpoint_data[0]['o']
    if objectt == connection:
        if con_is_var:
            objectt = con_var
            variables.append(objectt)
        else:
            objectt = dh.DataHandler().get_object_string(objectt)
    else:
        if random.random() <= var_prob:
            objectt = '?o'
            variables.append(objectt)
        else:
            objectt = dh.DataHandler().get_object_string(objectt)

    for elem in endpoint_data:
        subject = elem['s']
        predicate = elem['p']

        if random.random() <= var_prob:
            predicate = '?p' + str(pred_var_counter)
            variables.append(predicate)
            pred_var_counter += 1
        else:
            predicate = '<' + predicate['value'] + '>'

        if elem['s'] == connection:
            if con_is_var:
                subject = con_var
                variables.append(subject)
            else:
                if subject['type'] == 'uri':
                    subject = '<' + subject['value'] + '>'
        else:
            if random.random() <= var_prob:
                subject = '?s' + str(subj_var_counter)
                variables.append(subject)
                subj_var_counter += 1
            else:
                if subject['type'] == 'uri':
                    subject = '<' + subject['value'] + '>'

        patterns.append(subject + ' ' + predicate + ' ' + objectt + ' .')

    return {"patterns": patterns, "variables": variables, "subj_counter": subj_var_counter, "pred_counter": pred_var_counter}


def create_triple_patterns_path(endpoint_data, var_prob, connection, con_is_var, con_var, pred_var_counter, obj_var_counter):
    """Creates the basic shape of the query while replacing constants with
    variables according to the variable probability"""

    patterns = []
    variables = []

    is_first = endpoint_data[0]
    temp_var = "?o"
    path_is_var = random.random() <= var_prob

    for elem in endpoint_data:
        subject = elem['s']
        predicate = elem['p']
        objectt = elem['o']

        if path_is_var and is_first == elem:
            if elem['s'] == connection:
                if con_is_var:
                    subject = con_var
                    variables.append(subject)
                else:
                    if subject['type'] == 'uri':
                        subject = '<' + subject['value'] + '>'
            else:
                subject = '?s'
                variables.append(subject)
        elif path_is_var:
            subject = temp_var
        else:
            if subject['type'] == 'uri':
                subject = '<' + subject['value'] + '>'

        if random.random() <= var_prob:
            predicate = '?p' + str(pred_var_counter)
            variables.append(predicate)
            pred_var_counter += 1
        else:
            predicate = '<' + predicate['value'] + '>'

        path_is_var = random.random() <= var_prob

        if elem['o'] == connection:
            if con_is_var:
                objectt = con_var
                variables.append(objectt)
            else:
                objectt = dh.DataHandler().get_object_string(objectt)
        elif path_is_var:
            objectt = '?o' + str(obj_var_counter)
            variables.append(objectt)
            temp_var = '?o' + str(obj_var_counter)
            obj_var_counter += 1
        else:
            objectt = dh.DataHandler().get_object_string(objectt)

        patterns.append(subject + ' ' + predicate + ' ' + objectt + ' .')

    return {"patterns": patterns, "variables": variables, "pred_counter": pred_var_counter, "obj_counter": obj_var_counter}


def generate_query(queries, triples, operator_prob, var_prob):
    """Generates query."""

    start_time = timer()
    all_queries = []
    try_counter = 0
    limit_tries = 20
    while len(all_queries) < queries:
        if try_counter > limit_tries:
            break
        try_counter += 1
        query = ''
        endpoint_data_result = dh.DataHandler().fetch_data_mixed(triples)
        endpoint_data_first = endpoint_data_result['first']
        endpoint_data_second = endpoint_data_result['second']
        endpoint_data = endpoint_data_first['patterns'] + endpoint_data_second['patterns']
        # print(endpoint_data)
        if len(endpoint_data) >= triples:
            print("ENDPOINT DATA: ", endpoint_data)
            connection = endpoint_data_result['connection']
            patternandvar = create_triple_patterns(endpoint_data_first, endpoint_data_second, var_prob, connection)
            patterns = patternandvar['patterns']  # patterns is a list of strings containing the triple patterns with size = n
            variables = patternandvar['variables']
            where = oh.create_operators(triples, operator_prob, patterns)
            select = oh.create_select_distinct(operator_prob)
            choosen_variables = oh.choose_select_variables(variables)
            query = select + " " + choosen_variables + " FROM <http://dbpedia.org> " + where
            all_queries.append(query)

    total_time = timer() - start_time
    return {"queries": all_queries, "exectime": total_time}
