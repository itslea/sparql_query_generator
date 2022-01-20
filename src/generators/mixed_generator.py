import random
import helpers.data_handler as dh
import helpers.operator_handler as oh
import os


class MixedGenerator:
    """Creates mixed queries by randomly concatenating two of the three shape-types (star-subject, star-object, path)."""

    def __init__(self, endpoint_url):
        self.url = endpoint_url
        self.dir_path = os.path.join(os.getcwd(), "src\\queries")

    def create_triple_patterns(self, data_first, data_second, var_prob, connection):
        """Creates the basic shape of the query while replacing constants with
        variables according to the variable probability.

        :param data_first: list containing endpoint data for first shape
        :param data_second: list containing endpoint data for second shape
        :param var_prob: probability to replace triple constants with variables
        :param connection: contains connecting object

        :return: returns an object containing a list with triple patterns and a
                 list with all variables used in the triple patterns
        """

        subj_var_counter = 1  # counters make sure that no duplicate variables will be used in the patterns
        pred_var_counter = 1
        obj_var_counter = 1
        patterns = []
        variables = []

        con_var = "?connect"  # variable for connecting object
        con_is_var = random.random() <= var_prob  # decides if connecting object is variable

        if con_is_var:
            variables.append(con_var)

        # creates triple patterns for first shape
        if data_first['shape'] == "star_subject":
            patterns_and_var = self.create_triple_patterns_subject(data_first['data'], var_prob, connection, con_is_var, con_var, pred_var_counter, obj_var_counter)
            pred_var_counter = patterns_and_var['pred_counter']
            obj_var_counter = patterns_and_var['obj_counter']
        elif data_first['shape'] == "star_object":
            patterns_and_var = self.create_triple_patterns_object(data_first['data'], var_prob, connection, con_is_var, con_var, pred_var_counter, subj_var_counter)
            subj_var_counter = patterns_and_var['subj_counter']
            pred_var_counter = patterns_and_var['pred_counter']
        elif data_first['shape'] == "path":
            patterns_and_var = self.create_triple_patterns_path(data_first['data'], var_prob, connection, con_is_var, con_var, pred_var_counter, obj_var_counter)
            pred_var_counter = patterns_and_var['pred_counter']
            obj_var_counter = patterns_and_var['obj_counter']

        patterns += patterns_and_var['patterns']
        variables += patterns_and_var['variables']

        patterns_and_var2 = []

        # creates triple patterns for second shape
        if data_second['shape'] == "star_subject":
            patterns_and_var2 = self.create_triple_patterns_subject(data_second['data'], var_prob, connection, con_is_var, con_var, pred_var_counter, obj_var_counter)
        elif data_second['shape'] == "star_object":
            patterns_and_var2 = self.create_triple_patterns_object(data_second['data'], var_prob, connection, con_is_var, con_var, pred_var_counter, subj_var_counter)
        elif data_second['shape'] == "path":
            patterns_and_var2 = self.create_triple_patterns_path(data_second['data'], var_prob, connection, con_is_var, con_var, pred_var_counter, obj_var_counter)

        patterns += patterns_and_var2['patterns']
        variables += patterns_and_var2['variables']

        return {'patterns': patterns, 'variables': variables}

    def create_triple_patterns_subject(self, data, var_prob, connection, con_is_var, con_var, pred_var_counter, obj_var_counter):
        """Creates the basic shape of the query while replacing constants with
        variables according to the variable probability.

        :param data: list containing endpoint data
        :param var_prob: probability to replace triple constants with variables
        :param connection: contains connecting object
        :param con_is_var: boolean to check if the connecting object should be a variable
        :param con_var: variable used for connecting object
        :param pred_var_counter: counter to avoid duplicate predicate variables
        :param obj_var_counter: counter to avoid duplicate object varibles

        :return: returns an object containing a list with triple patterns, a
                 list with all variables used in the triple patterns and predicate and object
                 variable counter
        """

        patterns = []
        variables = []
        subject = data[0]['s']

        if subject == connection:  # decides if subject is variable
            if con_is_var:
                subject = con_var
            else:
                if subject['type'] == "uri":
                    subject = "<" + subject['value'] + ">"
        else:
            if random.random() <= var_prob:
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

            if elem['o'] == connection:
                if con_is_var:
                    objectt = con_var
                else:
                    objectt = dh.DataHandler(self.url).get_object_string(objectt)
            else:
                if random.random() <= var_prob:  # decides if object is variable
                    objectt = "?o" + str(obj_var_counter)
                    variables.append(objectt)
                    obj_var_counter += 1
                else:
                    objectt = dh.DataHandler(self.url).get_object_string(objectt)

            patterns.append(subject + " " + predicate + " " + objectt + " .")

        return {'patterns': patterns, 'variables': variables, 'pred_counter': pred_var_counter, 'obj_counter': obj_var_counter}

    def create_triple_patterns_object(self, data, var_prob, connection, con_is_var, con_var, pred_var_counter, subj_var_counter):
        """Creates the basic shape of the query while replacing constants with
        variables according to the variable probability.

        :param data: list containing endpoint data
        :param var_prob: probability to replace triple constants with variables
        :param connection: contains connecting object
        :param con_is_var: boolean to check if the connecting object should be a variable
        :param con_var: variable used for connecting object
        :param pred_var_counter: counter to avoid duplicate predicate variables
        :param subj_var_counter: counter to avoid duplicate subject varibles

        :return: returns an object containing a list with triple patterns, a
                 list with all variables used in the triple patterns and predicate and subject
                 variable counter
        """

        patterns = []
        variables = []
        objectt = data[0]['o']

        if objectt == connection:
            if con_is_var:
                objectt = con_var
            else:
                objectt = dh.DataHandler(self.url).get_object_string(objectt)
        else:
            if random.random() <= var_prob:  # decides if object is variable
                objectt = "?o"
                variables.append(objectt)
            else:
                objectt = dh.DataHandler(self.url).get_object_string(objectt)

        for elem in data:
            subject = elem['s']
            predicate = elem['p']

            if random.random() <= var_prob:  # decides if predicate is variable
                predicate = "?p" + str(pred_var_counter)
                variables.append(predicate)
                pred_var_counter += 1
            else:
                predicate = "<" + predicate['value'] + ">"

            if elem['s'] == connection:
                if con_is_var:
                    subject = con_var
                else:
                    if subject['type'] == "uri":
                        subject = "<" + subject['value'] + ">"
            else:
                if random.random() <= var_prob:  # decides if subject is variable
                    subject = "?s" + str(subj_var_counter)
                    variables.append(subject)
                    subj_var_counter += 1
                else:
                    if subject['type'] == "uri":
                        subject = "<" + subject['value'] + ">"

            patterns.append(subject + " " + predicate + " " + objectt + " .")

        return {'patterns': patterns, 'variables': variables, 'subj_counter': subj_var_counter, 'pred_counter': pred_var_counter}

    def create_triple_patterns_path(self, data, var_prob, connection, con_is_var, con_var, pred_var_counter, obj_var_counter):
        """Creates the basic shape of the query while replacing constants with
        variables according to the variable probability.

        :param data: list containing endpoint data
        :param var_prob: probability to replace triple constants with variables
        :param connection: contains connecting object
        :param con_is_var: boolean to check if the connecting object should be a variable
        :param con_var: variable used for connecting object
        :param pred_var_counter: counter to avoid duplicate predicate variables
        :param obj_var_counter: counter to avoid duplicate object varibles

        :return: returns an object containing a list with triple patterns, a
                 list with all variables used in the triple patterns and predicate and object
                 variable counter
        """

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
                if elem['s'] == connection:
                    if con_is_var:
                        subject = con_var
                    else:
                        if subject['type'] == "uri":
                            subject = "<" + subject['value'] + ">"
                else:
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

            if elem['o'] == connection:
                if con_is_var:
                    objectt = con_var
                else:
                    objectt = dh.DataHandler(self.url).get_object_string(objectt)
            elif path_is_var:
                objectt = "?o" + str(obj_var_counter)
                variables.append(objectt)
                temp_var = "?o" + str(obj_var_counter)
                obj_var_counter += 1
            else:
                objectt = dh.DataHandler(self.url).get_object_string(objectt)

            patterns.append(subject + " " + predicate + " " + objectt + " .")

        return {'patterns': patterns, 'variables': variables, 'pred_counter': pred_var_counter, 'obj_counter': obj_var_counter}

    def generate_query(self, queries, triples, operator_prob, var_prob):
        """Generates entire query. See also the READ_ME file.

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
            endpoint_data_result = dh.DataHandler(self.url).fetch_data_mixed(triples)
            endpoint_data_first = endpoint_data_result['first']  # contains data for first shape
            endpoint_data_second = endpoint_data_result['second']  # contains data for second shape
            endpoint_data = endpoint_data_first['data'] + endpoint_data_second['data']
            print(endpoint_data)
            if len(endpoint_data) >= triples:
                connection = endpoint_data_result['connection']  # connecting object needed for variable replacement
                patternandvar = self.create_triple_patterns(endpoint_data_first, endpoint_data_second, var_prob, connection)
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
        with open(os.path.join(self.dir_path, "mixed_queries.rq"), "w", encoding="utf-8") as file:
            file.write(query_string)

        return all_queries
