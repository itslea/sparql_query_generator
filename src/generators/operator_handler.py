import random


def choose_select_variables(variables):
    """Chooses random variables for SELECT (DISTINCT)"""

    choosen_variables = ""
    all_or_variables = ["all", "variables"]
    choose_all = random.choice(all_or_variables)
    if choose_all[0] == "all":
        choosen_variables = "*"
    else:
        random_variables = random.sample(variables, k=random.randint(1, len(variables) - 1))
        for elem in random_variables:
            if not random_variables.index(elem) == len(random_variables) - 1:
                choosen_variables += elem + ", "
            else:
                choosen_variables += elem

    return choosen_variables


def create_select_distinct(operator_prob):
    """Creates string for SELECT (DISTINCT)"""
    if random.random() <= operator_prob:
        return "SELECT DISTINCT"
    else:
        return "SELECT"


def create_union_string(union_patterns):
    """Creates string for UNION operator"""

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
    """Creates string for OPTIONAL operator"""

    optional_str = "OPTIONAL { "
    for elem in optional_patterns:
        optional_str += elem + " "
    optional_str += "} "

    return optional_str


def create_shape_string(rest_patterns):
    """Creates string for SHAPE criteria"""
    rest_str = ""
    for elem in rest_patterns:
        rest_str += elem + " "

    return rest_str


def create_operators(triples, operator_prob, patterns):
    """Creates the operators UNION and DISTINCT."""
    where_str = "WHERE { "
    bool_optional = False
    bool_union = False

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

    if bool_optional and bool_union:
        choose_first = ["optional", "union"]
        first = random.choice(choose_first)

        # Divide patterns by 3 -> optional, union, rest
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

            where_str += create_shape_string(rest_patterns) + create_optional_string(optional_patterns) + create_union_string(union_patterns)
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

    else:
        where_str += create_shape_string(patterns)

    where_str += "}"
    return where_str
