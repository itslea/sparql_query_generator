import random
from timeit import default_timer as timer
import generators.star_subject_generator as ssg
import generators.star_object_generator as sog
import generators.path_generator as pg
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

    con_var = "?o"
    con_is_var = random.random() <= var_prob

    patterns_and_var = []
    endpoint_patterns_first = []
    for elem in endpoint_data_first['patterns']:
        endpoint_patterns_first.append(elem)

    endpoint_patterns_second = []
    for elem in endpoint_data_second['patterns']:
        endpoint_patterns_second.append(elem)

    endpoint_patterns_connection = []
    endpoint_patterns_connection.append(endpoint_patterns_first[len(endpoint_data_first['patterns']) - 1])
    endpoint_patterns_connection.append(endpoint_patterns_second[0])

    endpoint_patterns_first.pop(len(endpoint_data_first['patterns']) - 1)
    endpoint_patterns_second.pop(0)

    if endpoint_data_first['shape'] == "star_subject":
        patterns_and_var = ssg.create_triple_patterns(endpoint_patterns_first, var_prob, pred_var_counter, obj_var_counter)
        pred_var_counter = patterns_and_var['pred_counter']
        obj_var_counter = patterns_and_var['obj_counter']
    elif endpoint_data_first['shape'] == "star_object":
        patterns_and_var = sog.create_triple_patterns(endpoint_patterns_first, var_prob, subj_var_counter, pred_var_counter)
        subj_var_counter = patterns_and_var['subj_counter']
        pred_var_counter = patterns_and_var['pred_counter']
    elif endpoint_data_first['shape'] == "path":
        patterns_and_var = pg.create_triple_patterns(endpoint_patterns_first, var_prob, pred_var_counter, obj_var_counter)
        pred_var_counter = patterns_and_var['pred_counter']
        obj_var_counter = patterns_and_var['obj_counter']

    patterns += patterns_and_var['patterns']
    variables += patterns_and_var['variables']

    for elem in endpoint_patterns_connection:
        subject = elem['s']
        predicate = elem['p']
        objectt = elem['o']

        if elem['s'] == connection:
            if con_is_var:
                subject = con_var
                variables.append(subject)
            else:
                if subject['type'] == 'uri':  # TODO: elif(subject['type' == ]) blank node
                    subject = '<' + subject['value'] + '>'
        else:
            if random.random() <= var_prob:
                subject = '?s' + str(pred_var_counter)
                variables.append(subject)
                subj_var_counter += 1
            else:
                if subject['type'] == 'uri':  # TODO: elif(subject['type' == ]) blank node
                    subject = '<' + subject['value'] + '>'

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

    if endpoint_data_second['shape'] == "star_subject":
        patterns_and_var = ssg.create_triple_patterns(endpoint_patterns_second, var_prob, pred_var_counter, obj_var_counter)
    elif endpoint_data_second['shape'] == "star_object":
        patterns_and_var = sog.create_triple_patterns(endpoint_patterns_second, var_prob, subj_var_counter, pred_var_counter)
    elif endpoint_data_second['shape'] == "path":
        patterns_and_var = pg.create_triple_patterns(endpoint_patterns_second, var_prob, pred_var_counter, obj_var_counter)

    patterns += patterns_and_var['patterns']
    variables += patterns_and_var['variables']

    print("WAS ", patterns)
    return {"patterns": patterns, "variables": variables}


def generate_query(queries, triples, operator_prob, var_prob):
    """Generates query."""

    start_time = timer()
    all_queries = []
    try_counter = 0
    limit_tries = 100
    while len(all_queries) < queries:
        if try_counter > limit_tries:
            break
        query = ''
        endpoint_data_result = dh.DataHandler().fetch_data_mixed(triples)
        endpoint_data_first = endpoint_data_result['first']
        endpoint_data_second = endpoint_data_result['second']
        endpoint_data = endpoint_data_first['patterns'] + endpoint_data_second['patterns']
        print(endpoint_data)
        if len(endpoint_data) >= triples:
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
