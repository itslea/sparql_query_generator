import random
import helpers.data_handler as dh
import helpers.operator_handler as oh
import os


class PathGenerator:
    """Creates path shaped SPARQL queries."""

    def __init__(self, endpoint_url):
        self.url = endpoint_url
        self.dir_path = os.path.join(os.getcwd(), "src\\queries")

    def create_triple_patterns(self, data, var_prob):
        """Creates the basic shape of the query while replacing constants with
        variables according to the variable probability.

        :param data: list containing endpoint data
        :param var_prob: probability to replace triple constants with variables

        :return: returns an object containing a list with triple patterns and a
                 list with all variables used in the triple patterns
        """

        pred_var_counter = 1
        obj_var_counter = 1

        patterns = []
        variables = []

        is_first = data[0]
        temp_var = "?o"
        path_is_var = random.random() <= var_prob  # makes sure path connecting constants (object and then subject) are both either variable or not

        for elem in data:
            subject = elem['s']
            predicate = elem['p']
            objectt = elem['o']

            if path_is_var and is_first == elem:
                subject = "?s"
                variables.append(subject)
            elif path_is_var:
                subject = temp_var
            else:
                if subject['type'] == "uri":
                    subject = "<" + subject['value'] + ">"

            if random.random() <= var_prob:
                predicate = "?p" + str(pred_var_counter)
                variables.append(predicate)
                pred_var_counter += 1
            else:
                predicate = "<" + predicate['value'] + ">"

            path_is_var = random.random() <= var_prob  # new variable decision for next part of path

            if path_is_var:
                objectt = "?o" + str(obj_var_counter)
                variables.append(objectt)
                temp_var = "?o" + str(obj_var_counter)
                obj_var_counter += 1
            else:
                objectt = dh.DataHandler(self.url).get_object_string(objectt)

            patterns.append(subject + " " + predicate + " " + objectt + " .")

        return {'patterns': patterns, 'variables': variables}

    def generate_query(self, queries, triples, operator_prob, var_prob):
        """Generates entire query.See also the READ_ME file.

        :param queries: number of queries to be generated
        :param triples: number of triple patterns for each query
        :param operator_prob: probability that operators will be used in the query
        :param var_prob: probability that constants will be replaced with variables

        :return: returns a list containing the queries
        """

        all_queries = []
        try_counter = 0
        limit_tries = 10000
        while len(all_queries) < queries:
            if try_counter > limit_tries:
                break
            try_counter += 1
            query = ""
            endpoint_data = dh.DataHandler(self.url).fetch_data_path(triples, False)
            if len(endpoint_data) >= triples:
                patternandvar = self.create_triple_patterns(endpoint_data, var_prob)
                patterns = patternandvar['patterns']  # patterns is a list of strings containing the triple patterns
                variables = patternandvar['variables']  # contains all variables used in triple pattern creation needed for SELECT
                where = oh.OperatorHandler().create_operators(triples, operator_prob, patterns)
                select = oh.OperatorHandler().create_select_distinct(operator_prob)
                choosen_variables = oh.OperatorHandler().choose_select_variables(variables)
                query = select + " " + choosen_variables + " FROM <http://dbpedia.org> " + where
                all_queries.append(query)

        # writes all queries to a file in folder 'queries'
        query_string = ""
        for query in all_queries:
            query_string += str(query) + "\n"
        with open(os.path.join(self.dir_path, "path_queries.rq"), "w", encoding="utf-8") as file:
            file.write(query_string)

        return all_queries
