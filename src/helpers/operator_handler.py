import random


class OperatorHandler:
    """Creates the operators used in sparql queries based on given probability."""

    def choose_select_variables(self, variables):
        """Chooses random variables for SELECT (DISTINCT).

        :param variables: list containing variables used in the triple patterns

        :return: returns a list containing choosen variables
        """

        choosen_variables = ""
        all_or_variables = ["all", "variables"]
        choose_all = str(random.choice(all_or_variables))
        if len(variables) <= 0:
            choose_all = "all"
        if choose_all == "all":
            choosen_variables = "*"
        else:
            var_size = len(variables)
            if len(variables) > 10:
                var_size = 10  # maximum of 10 selected variables
            random_variables = random.sample(variables, k=random.randint(1, var_size))  # k=random.randint(1, len(variables)) if you want to be able to select all variables
            for elem in random_variables:
                if not random_variables.index(elem) == len(random_variables) - 1:
                    choosen_variables += elem + ", "
                else:
                    choosen_variables += elem

        return choosen_variables

    def create_select_distinct(self, operator_prob):
        """Creates string for SELECT (DISTINCT).

        :param operator_prob: probability that operators will be used in the query

        :return: returns SELECT or SELECT DISTINCT string
        """

        if random.random() <= operator_prob:
            return "SELECT DISTINCT"
        else:
            return "SELECT"

    def create_union_string(self, union_patterns):
        """Creates string for UNION operator.

        :param union_patterns: list containing patterns used for UNION

        :return: returns the UNION string
        """

        union_str = "{ "
        part1_len = random.randint(1, len(union_patterns) - 1)

        for i in range(0, part1_len):
            union_str += union_patterns[i] + " "
        union_str += "} UNION { "
        for i in range(part1_len, len(union_patterns)):
            union_str += union_patterns[i] + " "
        union_str += "} "

        return union_str

    def create_optional_string(self, optional_patterns):
        """Creates string for OPTIONAL operator.
        
        :param optional_patterns: list containing patterns used for OPTIONAL

        :return: returns the OPTIONAL string
        """

        optional_str = "OPTIONAL { "
        for elem in optional_patterns:
            optional_str += elem + " "
        optional_str += "} "

        return optional_str

    def create_shape_string(self, rest_patterns):
        """Creates string for SHAPE criteria.

        :param rest_patterns: list containing patterns used neither in OPTIONAL nor UNION

        :return: returns the rest string
        """

        rest_str = ""
        for elem in rest_patterns:
            rest_str += elem + " "

        return rest_str

    def create_operators(self, triples, operator_prob, patterns):
        """Creates the operators UNION and DISTINCT.

        :param triples: number of triple patterns for each query
        :param operator_prob: probability that operators will be used in the query
        :param patterns: list containing the triple patterns

        :return: returns entire WHERE string
        """

        where_str = "WHERE { "
        bool_optional = False
        bool_union = False

        # decides which operators to use (or both)
        if triples >= 3:
            if random.random() <= operator_prob:
                bool_optional = True
            if random.random() <= operator_prob:
                bool_union = True
        else:
            if triples == 2:
                if random.random() <= operator_prob:
                    bool_union = True
            elif triples == 1:
                if random.random() <= operator_prob:
                    bool_optional = True

        # case: OPTIONAL and UNION
        if bool_optional and bool_union:
            # decides if UNION or OPTIONAL should be first in query
            choose_first = ["optional", "union"]
            first = random.choice(choose_first)

            # divide patterns by 3 -> optional, union, rest of query
            if first[0] == "optional":
                o = random.randint(1, triples - 2)
                u = random.randint(2, triples - o)
                r = triples - o - u

                rest_patterns = []
                for i in range(0, r):
                    rest_patterns.append(patterns[i])

                optional_patterns = []
                for i in range(r, r + o):
                    optional_patterns.append(patterns[i])

                union_patterns = []
                for i in range(r + o, triples):
                    union_patterns.append(patterns[i])

                where_str += self.create_shape_string(rest_patterns) + self.create_optional_string(optional_patterns) + self.create_union_string(union_patterns)
            else:
                u = random.randint(2, triples - 1)
                o = random.randint(1, triples - u)
                r = triples - o - u

                rest_patterns = []
                for i in range(0, r):
                    rest_patterns.append(patterns[i])

                union_patterns = []
                for i in range(r, r + u):
                    union_patterns.append(patterns[i])

                optional_patterns = []
                for i in range(r + u, triples):
                    optional_patterns.append(patterns[i])

                where_str += self.create_shape_string(rest_patterns) + self.create_union_string(union_patterns) + self.create_optional_string(optional_patterns)
        # case: OPTIONAL
        elif bool_optional:
            o = random.randint(1, triples)
            r = triples - o

            rest_patterns = []
            for i in range(0, r):
                rest_patterns.append(patterns[i])

            optional_patterns = []
            for i in range(r, triples):
                optional_patterns.append(patterns[i])

            where_str += self.create_shape_string(rest_patterns) + self.create_optional_string(optional_patterns)
        # case: UNION
        elif bool_union:
            u = random.randint(2, triples)
            r = triples - u

            rest_patterns = []
            for i in range(0, r):
                rest_patterns.append(patterns[i])

            union_patterns = []
            for i in range(r, triples):
                union_patterns.append(patterns[i])

            where_str += self.create_shape_string(rest_patterns) + self.create_union_string(union_patterns)

        else:
            where_str += self.create_shape_string(patterns)

        where_str += "}"
        return where_str
