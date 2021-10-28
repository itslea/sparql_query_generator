import sys
import random
import pandas as pd
from collections import OrderedDict
import requests
import argparse

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
    parser.add_argument("-sub", "--subject",
                        help="probability to add a constant subject in a triple pattern", type=float)
    parser.add_argument("-ob", "--object",
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

    return args.server, args.graph, args.queries, args.file, args.subject, args.object, args.size



def add_subject_constant(url, dataset, p, o):

    """

    This function finds a random constant for the subject position given a predicate p and an object o.
    Only for the  first triple in the path.
    :return: one random subject-constant

    """

    querySubject = "SELECT ?s " + dataset + " WHERE { ?s <" + p + "> " + o + " . }"
    reqSubject = requests.get(url, params={'format': 'json', 'query': querySubject})
    dataSubject = reqSubject.json()

    subject = []
    for itemSubj in dataSubject['results']['bindings']:
        subject.append(itemSubj['s']['value'])

    if len(subject) > 1:
        s = random.sample(subject, 1)[0]
    if len(subject) == 1:
        s = subject[0]

    return s




def get_first_path(url, dataset):


    """

    This function retrieves a random fraction of the dataset with predicates and objects,
    where the object continues with a path,
    accessed via the URL of the endpoint.
    We only retrieve a fraction to make this query generator perform very fast.
    :return: list with predicates and objects in a dictionary

    """

    query_path = "SELECT DISTINCT ?p ?o "+dataset+" WHERE {?s ?p ?o. ?o ?p2 ?o2.  FILTER(?p != rdf:type) FILTER(1 > <SHORT_OR_LONG::bif:rnd> (1000, ?s, ?p, ?o))}"

    req_path = requests.get(url, params={'format': 'json', 'query': query_path})
    data_path = req_path.json()

    path = []
    for items in data_path['results']['bindings']:
        o = items['o']['value']
        o = "<" + o + ">"
        p = items['p']['value']

        path.append({'p': p, 'o': o})

    return path


def get_next_path(url, dataset, s):


    """

    This function retrieves one triple for the middle part of path,
    starting point is the subject (or object of path before).
    There must be another triple following to continue the path.
    accessed via the URL of the endpoint.
    :return: list with predicates and objects in a dictionary

    """

    query_path = "SELECT DISTINCT ?p ?o "+dataset+" WHERE { " + s + " ?p ?o. ?o ?p2 ?o2. FILTER(?p != rdf:type) }"

    req_path = requests.get(url, params={'format': 'json', 'query': query_path})
    data_path = req_path.json()

    path = []
    for items in data_path['results']['bindings']:
        o = items['o']['value']
        o = "<" + o + ">"

        p = items['p']['value']

        path.append({'p': p, 'o': o})

    if len(path) > 1:
        res = random.sample(path, 1)[0]
    if len(path) == 1:
        res = path[0]
    if len(path) == 0:
        raise ValueError

    res = random.sample(path, 1)[0]

    p = res['p']
    o = res['o']

    return p, o



def get_last_path(url, dataset, s):


    """

    This function retrieves the last triple of the path, with a fixed subject,
    accessed via the URL of the endpoint.
    :return: predicate and object of last triple of path

    """

    add_object = True

    query_path = "SELECT DISTINCT ?p ?o "+dataset+" WHERE { " + s + " ?p ?o. FILTER(?p != rdf:type) }"

    req_path = requests.get(url, params={'format': 'json', 'query': query_path})
    data_path = req_path.json()

    path = []
    for items in data_path['results']['bindings']:

        p = items['p']['value']

        o = items['o']['value']
        if 'literal' in items['o']['type']:
            o = repr(o)
            o = o.strip("'")
            o = o.rstrip("'")
            o = o.replace('"', '\\"')
            o = '"' + o + '"'
        if 'datatype' in items['o'].keys():
            # This is added to handle Virtuoso 06 issues evaluating dates.
            if 'date' in items['o']['datatype']:
                add_object = False
            o = o + '^^<' + items['o']['datatype'] + ">"
        if 'xml:lang' in items['o'].keys():
            o = o + '@' + items['o']['xml:lang']

        path.append({'p': p, 'o': o})

    if len(path) > 1:
        res = random.sample(path, 1)[0]
    if len(path) == 1:
        res = path[0]

    p = res['p']
    obj = res['o']

    if obj[:4] == "http":
        o = "<" + obj + ">"
    else:
        o = obj

    return p, o, add_object


def generate_path(url, queryNumber, fileName, dataset, subject_prob, object_prob, n):

    """
    This functions generates the queries!
    :param url: the url of the SPARQL endpoint
    :param queryNumber: required amount of queries that should be generated
    :param fileName: the name of the output file
    :param dataset: only this graph will be used to generate the queries
    :param subject_prob: probability of having a constant on subject position in first triple of path. e.g. 0.5 gives a 50 % chance
    :param object_prob: probability of having a constant on object position in last triple of path. e.g. 0.5 gives a 50 % chance
    :param n: amount of triples in each query
    :return: file with created SPARQL queries

    """

    f = open(fileName, "w")

    # saves the created queries in order to avoid duplicates:
    created_queries = []

    # counts the created queries:
    count = 0
    tries = 0

    # saves used predicates in order to avoid duplicates early on:
    #predicates_used = []


    while count < queryNumber and tries < maxTriesTotal:


        path = get_first_path(url, dataset)
        tries = tries + 1

        for queryIterations in range(min(queryNumber-count, len(path))):

            can_q = set()

            res = path.pop(0)  # res = random.sample(path, 1)[0]

            p = res['p']
            o = res['o']

            queryLinePrint = "SELECT * WHERE {"

            # creates first triple :

            if random.random() <= subject_prob:
                s = add_subject_constant(url, dataset, p, o)
                queryLinePrint = queryLinePrint + " <" + s + "> <" + p + "> ?o1 ."
                can_q.add((s, p))
            else:
                queryLinePrint = queryLinePrint + " ?s1 <" + p + "> ?o1 ."
                can_q.add((p))


            # creates all triples in between first and last:

            if n > 2:

                stopIteration = False

                for k in range(2, n):
                    s = o
                    try:
                        p, o = get_next_path(url, dataset, s)
                        queryLinePrint = queryLinePrint + " ?o" + str(k - 1) + " <" + p + "> ?o" + str(k) + " ."
                        can_q.add((p))
                    except ValueError:
                        stopIteration = True
                        break

                if stopIteration:
                    continue # question: does this break the iteration and goes back up to the next queryIteration ?



            # creates last triple:

            s = o
            p, o, add_object = get_last_path(url, dataset, s)

            if random.random() <= object_prob and add_object:

                queryLinePrint = queryLinePrint + " ?o" + str(n-1) + " <" + p + "> " + o + " ."
                can_q.add((p, o))
            else:
                queryLinePrint = queryLinePrint + " ?o" + str(n-1) + " <" + p + "> ?o" + str(n) + " ."
                can_q.add((p))


            queryLinePrint = queryLinePrint + "}\n"

            if can_q not in created_queries:
                print(queryLinePrint)
                f.write(queryLinePrint)
                created_queries.append(can_q)
                count = count + 1

    f.close()

if __name__ == '__main__':
    (server, graph, queries, file, subject, object, n) = get_options()

    dataset = ''
    if graph:
        dataset = "FROM " + graph

    generate_path(server, queries, file, dataset, subject, object, n)
    print("Queries are generated!")


####### TERMINAL EXAMPLE: python3 elena_path_generator.py -s http://129.13.152.179:8892/sparql -g "<http://localhost/drugbank>" -n 2 -q 1 -f path_test.rq -ob 0.5