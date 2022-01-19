import random
import helpers.data_handler as dh
import helpers.operator_handler as oh


class StarObjectGenerator:
    """Creates star-object shaped SPARQL queries"""

    def __init__(self, endpoint_url):
        self.url = endpoint_url

    def create_triple_patterns(self, data, var_prob):
        """Creates the basic shape of the query while replacing constants with
        variables according to the variable probability"""

        subj_var_counter = 1
        pred_var_counter = 1

        patterns = []
        variables = []

        objectt = data[0]['o']
        if random.random() <= var_prob:
            objectt = "?o"
            variables.append(objectt)
        else:
            objectt = dh.DataHandler(self.url).get_object_string(objectt)

        for elem in data:
            subject = elem['s']
            predicate = elem['p']

            if random.random() <= var_prob:
                predicate = "?p" + str(pred_var_counter)
                variables.append(predicate)
                pred_var_counter += 1
            else:
                predicate = "<" + predicate['value'] + ">"

            if random.random() <= var_prob:
                subject = "?s" + str(subj_var_counter)
                variables.append(subject)
                subj_var_counter += 1
            else:
                if subject['type'] == "uri":
                    subject = "<" + subject['value'] + ">"

            patterns.append(subject + " " + predicate + " " + objectt + " .")

        return {'patterns': patterns, 'variables': variables}

    def generate_query(self, queries, triples, operator_prob, var_prob):
        """Generates query."""
        all_queries = []
        try_counter = 0
        limit_tries = 10000
        while len(all_queries) < queries:
            if try_counter > limit_tries:
                break
            try_counter += 1
            query = ""
            endpoint_data = dh.DataHandler(self.url).fetch_data_object(triples)
            if len(endpoint_data) >= triples:
                patternandvar = self.create_triple_patterns(endpoint_data, var_prob)
                patterns = patternandvar['patterns']  # patterns is a list of strings containing the triple patterns with size = n
                variables = patternandvar['variables']
                where = oh.OperatorHandler().create_operators(triples, operator_prob, patterns)
                select = oh.OperatorHandler().create_select_distinct(operator_prob)
                choosen_variables = oh.OperatorHandler().choose_select_variables(variables)
                query = select + " " + choosen_variables + " FROM <http://dbpedia.org> " + where
                all_queries.append(query)
        return all_queries
