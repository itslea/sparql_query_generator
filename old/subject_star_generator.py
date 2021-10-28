import sys
import random
import pandas as pd
from collections import OrderedDict
import requests
import argparse
import time

# Increase this parameter if trying generating many queries.
maxTriesTotal = 1000

def get_options():

    parser = argparse.ArgumentParser(description="SPARQL query generator")

    parser.add_argument("-s", "--server",
                        help="URL of the SPARQL endpoint (required)")
    parser.add_argument("-g", "--graph",
                        help="RDF graph used to generate the queries")
    parser.add_argument("-n", "--size",
                        help="number of triple patterns per query", type=int)
    parser.add_argument("-q", "--queries",
                        help="number of queries to generate", type=int)
    parser.add_argument("-f", "--file",
                        help="output file")
    parser.add_argument("-o", "--object",
                        help="probability to add a constant object in a triple pattern", type=float)
    args = parser.parse_args()

    # Handling mandatory arguments.
    err = False
    msg = []
    if not args.server:
        err = True
        msg.append("error: no server specified. Use argument -s to specify the address of a SPARQL endpoint.")

    if err:
        parser.print_usage()
        print("\n".join(msg))
        sys.exit(1)

    return args.server, args.graph, args.size, args.queries, args.file, args.object





def add_object_constant(url, dataset, s, p):

    """

    This function finds a random constant for the object position given a subject s and a predicate p.
    :return: one random object-constant


    """

    queryObject = "SELECT ?o " + dataset + " WHERE { <" + s + "> <" + p + "> ?o . }"
    reqObject = requests.get(url, params={'format': 'json', 'query': queryObject})
    dataObject = reqObject.json()

    object = []
    for itemObj in dataObject['results']['bindings']:
        o = itemObj['o']['value']
        # print("o", o)
        if 'literal' in itemObj['o']['type']:
            o = repr(o)
            o = o.strip("'")
            o = o.rstrip("'")
            o = o.replace('"', '\\"')
            o = '"' + o + '"'
        if 'datatype' in itemObj['o'].keys():
            # This is added to handle Virtuoso 06 issues evaluating dates.
            if 'date' in itemObj['o']['datatype']:
                raise ValueError
            o = o + '^^<' + itemObj['o']['datatype'] + ">"
        if 'xml:lang' in itemObj['o'].keys():
            o = o + '@' + itemObj['o']['xml:lang']
        object.append(o)

    obj = random.sample(object, 1)[0]

    if obj[:4] == "http":
        o = "<" + obj + ">"
    else:
        o = obj

    return o


def get_subjects(url, dataset):

    """

    This function retrieves a random fraction of all subjects, that have at least 2 predicates, of the dataset,
    accessed via the URL of the endpoint.
    We only retrieve a fraction to make this query generator perform very fast.
    :return: list with subjects

    """

    querySubjects = "SELECT DISTINCT ?s " + dataset + " WHERE {?s ?p1 ?o1. ?s ?p2 ?o2. FILTER(?p1 < ?p2) FILTER(1 > <SHORT_OR_LONG::bif:rnd> (1000, ?s, ?p1, ?o1))}"
    reqSubjects = requests.get(url, params={'format': 'json', 'query': querySubjects})
    dataSubjects = reqSubjects.json()

    subjects = []
    for itemSubj in dataSubjects['results']['bindings']:
        subjects.append(itemSubj['s']['value'])

    return subjects



def generate_star_subject(url, triples, queries, fileName, dataset, object_prob):

    """

    This functions generates the queries!
    :param url:  the url of the SPARQL endpoint
    :param triples: amount of triples in each query
    :param queries: required amount of queries that should be generated
    :param fileName: the name of the output file
    :param dataset: only this graph will be used to generate the queries
    :param object_prob: probability of having a constant on object position, e.g. 0.5 gives a 50 % chance
    :return: file with created SPARQL queries

    """

    f = open(fileName, "w")

    # saves the created queries in order to avoid duplicates:
    created_queries = []

    # counts the created queries:
    count = 0
    tries = 0

    while count < queries and tries < maxTriesTotal:

        # retrieves a new fraction of subjects:
        subjects = get_subjects(url, dataset)
        n = len(subjects)
        tries += 1

        for queryIterations in range(min(queries - count, n)):

            # choose a random subject from the fraction of subjects:
            s = subjects.pop(0) #random.sample(subjects, 1)[0]

            # retrieve all predicates of the chosen subject:
            queryPredicates = "SELECT distinct ?p " + dataset + " WHERE { <" + s + "> ?p ?o. } "
            reqPredicates = requests.get(url, params={'format': 'json', 'query': queryPredicates})
            dataPredicates = reqPredicates.json()

            predicates = []
            for itemPred in dataPredicates['results']['bindings']:
                predicates.append(itemPred['p']['value'])

            # amount of predicates:
            lenP = len(predicates)

            # only if the amount of predicates is higher than the requested amount of triples, the triple can be created:

            if lenP >= triples:

                # chooses randomly the amount of requires predicates = amount of triples:
                preds = random.sample(predicates, k = triples)

                # starts building the query:
                queryLinePrint = "SELECT * WHERE {"

                can_q = set()
                # creates the triples:
                for triple in range(triples):

                    # chooses p from the list
                    p = preds[triple]

                    # adds a constant on object position - if probability is given:
                    if random.random() <= object_prob:
                        try:
                            o = add_object_constant(url, dataset, s, p)
                            queryLinePrint = queryLinePrint + " ?s <" + p + "> " + o + " ."
                            can_q.add((p, o))
                        except ValueError:
                            queryLinePrint = queryLinePrint + " ?s <" + p + "> ?o" + str(triple + 1) + " ."
                            can_q.add((p))

                    # otherwise there is a variable on object position:
                    else:
                        queryLinePrint = queryLinePrint + " ?s <" + p + "> ?o" + str(triple + 1) + " ."
                        can_q.add((p))

                queryLinePrint = queryLinePrint + "}\n"

                # checks of query is already created,
                # writes query to file and saves the query in created_queries,
                # and adds 1 to count:

                if can_q not in created_queries:
                    #print(queryLinePrint)
                    f.write(queryLinePrint)
                    created_queries.append(can_q)
                    count = count + 1
                    if count % 1000 == 0:
                        time.sleep(5)

    f.close()


if __name__ == '__main__':
    (server, graph, triples, queries, file, object) = get_options()

    dataset = ''
    if graph:
        dataset = "FROM " + graph
    generate_star_subject(server, triples, queries, file, dataset, object)
    print("Queries are generated!")



####### TERMINAL EXAMPLE: python3 elena_star_generator.py -s http://129.13.152.179:8892/sparql -g "<http://localhost/drugbank>" -n 2 -q 1 -f elena_new.rq -o 0.5