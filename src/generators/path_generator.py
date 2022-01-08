import random
from timeit import default_timer as timer
import helpers.data_handler as dh
import helpers.operator_handler as oh
import helpers.timetaker as tt


def create_triple_patterns(endpoint_data, var_prob):
    """Creates the basic shape of the query while replacing constants with
    variables according to the variable probability"""

    pred_var_counter = 1
    obj_var_counter = 1

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

        if path_is_var:
            objectt = '?o' + str(obj_var_counter)
            variables.append(objectt)
            temp_var = '?o' + str(obj_var_counter)
            obj_var_counter += 1
        else:
            objectt = dh.DataHandler().get_object_string(objectt)

        patterns.append(subject + ' ' + predicate + ' ' + objectt + ' .')

    return {"patterns": patterns, "variables": variables}


def generate_query(queries, triples, operator_prob, var_prob):
    """Generates query."""
    all_queries = []
    try_counter = 0
    limit_tries = 100
    while len(all_queries) < queries:
        if try_counter > limit_tries:
            break
        try_counter += 1
        query = ''
        endpoint_data = dh.DataHandler().fetch_data_path(triples)
        if len(endpoint_data) >= triples:
            timelogger.message_log(endpoint_data)
            patternandvar = create_triple_patterns(endpoint_data, var_prob)
            patterns = patternandvar['patterns']  # patterns is a list of strings containing the triple patterns with size = n
            variables = patternandvar['variables']
            where = oh.OperatorHandler().create_operators(triples, operator_prob, patterns)
            select = oh.OperatorHandler().create_select_distinct(operator_prob)
            choosen_variables = oh.OperatorHandler().choose_select_variables(variables)
            query = select + " " + choosen_variables + " FROM <http://dbpedia.org> " + where
            all_queries.append(query)
    return all_queries
