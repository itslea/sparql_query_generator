import random
import helpers.data_handler as dh
import helpers.operator_handler as oh
import os


class StarSubjectGenerator:
    """Creates star-subject shaped SPARQL queries."""

    def __init__(self, endpoint_url):
        self.url = endpoint_url
        self.dir_path = os.path.join(os.getcwd(), "src\\queries")

    def create_triple_patterns(self, data, var_prob):
        """Creates the basic shape of the query while replacing constants with
        variables according to the variable probability."""

        pred_var_counter = 1
        obj_var_counter = 1

        patterns = []
        variables = []
        subject = data[0]['s']

        if random.random() <= var_prob:  # decides if subject is variable
            subject = "?s"
            variables.append(subject)
        else:
            if subject['type'] == "uri":
                subject = "<" + subject['value'] + ">"

        for elem in data:
            predicate = elem['p']
            objectt = elem['o']

            if random.random() <= var_prob:  # decides if predicate is variable
                predicate = "?p" + str(pred_var_counter)
                variables.append(predicate)
                pred_var_counter += 1
            else:
                predicate = "<" + predicate['value'] + ">"

            if random.random() <= var_prob:  # decides if object is variable
                objectt = "?o" + str(obj_var_counter)
                variables.append(objectt)
                obj_var_counter += 1
            else:
                objectt = dh.DataHandler(self.url).get_object_string(objectt)

            patterns.append(subject + " " + predicate + " " + objectt + " .")

        return {'patterns': patterns, 'variables': variables}

    def generate_query(self, queries, triples, operator_prob, var_prob):
        """Generates entire query."""

        all_queries = []
        try_counter = 0
        limit_tries = 10000
        while len(all_queries) < queries:
            if try_counter > limit_tries:
                break
            try_counter += 1
            query = ""
            endpoint_data = dh.DataHandler(self.url).fetch_data_subject(triples, False)
            if len(endpoint_data) >= triples:
                patternandvar = self.create_triple_patterns(endpoint_data, var_prob)
                patterns = patternandvar['patterns']  # patterns is a list of strings containing the triple patterns
                variables = patternandvar['variables']  # contains all variables used in triple pattern creation needed for SELECT
                where = oh.OperatorHandler().create_operators(triples, operator_prob, patterns)
                select = oh.OperatorHandler().create_select_distinct(operator_prob)
                choosen_variables = oh.OperatorHandler().choose_select_variables(variables)
                query = select + " " + choosen_variables + " FROM <http://dbpedia.org> " + where
                all_queries.append(query)

        query_string = ""
        for query in all_queries:
            query_string += str(query) + "\n"
        with open(os.path.join(self.dir_path, "star_subject_queries.rq"), "w", encoding="utf-8") as file:
            file.write(query_string)

        return all_queries
