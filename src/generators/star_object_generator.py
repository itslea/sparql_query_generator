import random
import generators.data_handler as dh
import generators.operator_handler as oh


def create_triple_patterns(endpoint_data, var_prob):
    """Creates the basic shape of the query while replacing constants with
    variables according to the variable probability"""

    pred_var_counter = 1
    subj_var_counter = 1
    patterns = []
    variables = []

    objectt = endpoint_data[0]['o']
    if random.random() <= var_prob:
        objectt = '?o'
        variables.append(objectt)
    else:
        if objectt['type'] == 'uri':
            objectt = '<' + objectt['value'] + '>'
        elif objectt['type'] == 'literal':
            objectt = '\"' + objectt['value'] + '\"' + "@" + objectt['xml:lang']
        elif objectt['type'] == 'typed-literal':
            if objectt['datatype'] == 'http://www.w3.org/2001/XMLSchema#integer':
                objectt = str(objectt['value'])
            else:
                objectt = '\"' + objectt['value'] + '\"' + "^^<" + objectt['datatype'] + ">"
        # TODO: elif blank node

    for elem in endpoint_data:
        subject = elem['s']
        predicate = elem['p']

        if random.random() <= var_prob:
            predicate = '?p' + str(pred_var_counter)
            variables.append(predicate)
            pred_var_counter += 1
        else:
            predicate = '<' + predicate['value'] + '>'

        if random.random() <= var_prob:
            subject = '?s' + str(pred_var_counter)
            variables.append(subject)
            subj_var_counter += 1
        else:
            if subject['type'] == 'uri':
                subject = '<' + subject['value'] + '>'
            # TODO: elif(subject['type' == ]) blank node

        patterns.append(subject + ' ' + predicate + ' ' + objectt + ' .')

    return {"patterns": patterns, "variables": variables}


def generate_query(queries, triples, operator_prob, var_prob):
    """Generates query."""
    query = ''
    endpoint_data = dh.DataHandler().fetch_data_object(triples)
    if len(endpoint_data) >= triples:
        patternandvar = create_triple_patterns(endpoint_data, var_prob)
        patterns = patternandvar['patterns']  # patterns is a list of strings containing the triple patterns with size = n
        variables = patternandvar['variables']
        where = oh.create_operators(triples, operator_prob, patterns)
        select = oh.create_select_distinct(operator_prob)
        choosen_variables = oh.choose_select_variables(variables)
        query = select + " " + choosen_variables + " FROM <http://dbpedia.org> " + where
        return query

    else:
        print("STOP, ZU WENIG TRIPLE IN GRAPH")  # TODO: was passiert dann?
        return None
