import random


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
    bool_distinct = False
    bool_optional = False
    bool_union = False

    if triples >= 3:
        if random.random() <= operator_prob:
            bool_distinct = True
        if random.random() <= operator_prob:
            bool_optional = True
        if random.random() <= operator_prob:
            bool_union = True
    else:
        if triples == 2:
            if random.random() <= operator_prob:
                bool_distinct = True
            if random.random() <= operator_prob:
                bool_union = True
        elif triples == 1:
            if random.random() <= operator_prob:
                bool_distinct = True
            if random.random() <= operator_prob:
                bool_optional = True

    if bool_distinct:
        print("TODO")

    if bool_optional and bool_union:
        choose_first = ["optional", "union"]
        first = random.choices(choose_first)

        # Divide patterns by 3 -> optional, union, rest
        if first[0] == "optional":
            o = random.randint(1, triples - 2)
            u = random.randint(2, triples - o)
            r = triples - o - u

            rest_patterns = []
            for i in range(0, r):
                rest_patterns.append(patterns[i])
            print("rest " + str(r) + " :")
            print(rest_patterns)

            optional_patterns = []
            for i in range(r, r + o):
                optional_patterns.append(patterns[i])
            print("optional " + str(o) + " :")
            print(optional_patterns)

            union_patterns = []
            for i in range(r + o, triples):
                union_patterns.append(patterns[i])
            print("union " + str(u) + " :")
            print(union_patterns)

            where_str += create_shape_string(rest_patterns) + create_optional_string(optional_patterns) + create_union_string(union_patterns)
        else:
            u = random.randint(2, triples - 1)
            o = random.randint(1, triples - u)
            r = triples - o - u

            rest_patterns = []
            for i in range(0, r):
                rest_patterns.append(patterns[i])
            print("rest " + str(r) + " :")
            print(rest_patterns)

            union_patterns = []
            for i in range(r, r + u):
                union_patterns.append(patterns[i])
            print("union " + str(u) + " :")
            print(union_patterns)

            optional_patterns = []
            for i in range(r + u, triples):
                optional_patterns.append(patterns[i])
            print("optional " + str(o) + " :")
            print(optional_patterns)

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

    where_str += "}"
    return where_str
