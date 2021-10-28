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
                        help="probability to add a constant subject in a triple pattern", type=float)  # noqa: E501
    args = parser.parse_args()

    # Handling mandatory arguments.
    err = False
    msg = []
    if not args.server:
        err = True
        msg.append("error: no server specified. Use argument -s to specify the address of a SPARQL endpoint.")  # noqa: E501

    if err:
        parser.print_usage()
        print("\n".join(msg))
        sys.exit(1)

    return args.server, args.graph, args.queries, args.file, args.subject, args.size  # noqa: E501


def add_subject_constant(url, dataset, p, o):

    """

    This function finds a random constant for the subject position given a predicate p and an object o.  # noqa: E501
    :return: list with random subject-constants

    """

    querySubject = "SELECT ?s " + dataset + " WHERE { ?s <" + p + "> " + o + " . }"  # noqa: E501
    reqSubject = requests.get(url, params={'format': 'json', 'query': querySubject})  # noqa: E501
    dataSubject = reqSubject.json()

    subject = []
    for itemSubj in dataSubject['results']['bindings']:
        subject.append(itemSubj['s']['value'])

    return subject


def get_objects(url, dataset):


    """

    This function retrieves a random fraction of the dataset with predicates and objects, # noqa: E501
    the object has at least two different subjects with the same predicate.
    accessed via the URL of the endpoint.
    We only retrieve a fraction to make this query generator perform very fast.
    :return: list with predicates and objects in a dictionary

    """
    query_object = "SELECT DISTINCT ?p ?o "+dataset+" WHERE {?s1 ?p ?o. ?s2 ?p ?o. FILTER(?s1 <?s2) FILTER(?p != rdf:type) FILTER(1 > <SHORT_OR_LONG::bif:rnd> (1000, ?s1, ?p, ?o))}"  # noqa: E501

    req_object = requests.get(url, params={'format': 'json', 'query': query_object})  # noqa: E501
    #print(req_object)
    data_object = req_object.json()
    

    object = []
    for itemObj in data_object['results']['bindings']:
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
                continue
            o = o + '^^<' + itemObj['o']['datatype'] + ">"
        if 'xml:lang' in itemObj['o'].keys():
            o = o + '@' + itemObj['o']['xml:lang']
        object.append({'o': o, 'p': itemObj['p']['value']})

    return object


def generate_star_object(url, queryNumber, fileName, dataset, subject_prob, n):

    """
    This functions generates the queries!
    :param url: the url of the SPARQL endpoint
    :param queryNumber: required amount of queries that should be generated
    :param fileName: the name of the output file
    :param dataset: only this graph will be used to generate the queries
    :param subject_prob: probability of having a constant on subject position, e.g. 0.5 gives a 50 % chance  # noqa: E501
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
    # predicates_used = []


    while count < queryNumber and tries < maxTriesTotal:
        objects = get_objects(url, dataset)
        tries = tries + 1

        for queryIterations in range(min(queryNumber-count, len(objects))):
            res = objects.pop(0)  # res = random.sample(objects, 1)[0]
            p = res['p']
            obj = res['o']

            if obj[:4] == "http":
                o = "<" + obj + ">"
            else:
                o = obj

            #if p in predicates_used:
            #    print("p already used")
            #    continue

            #predicates_used.append(p)

            subject = add_subject_constant(url, dataset, p, o)

            #has_subject = True

            # try:
            #     subject = add_subject_constant(url, dataset, p, o)
            #     if not subject:
            #         has_subject = False
            # except ValueError:
            #     has_subject = False
            lenS = len(subject)

            if lenS > n:
            # Building the final query:
                queryLinePrint = "SELECT * WHERE {"
                can_q = set()

                for k in range(n):
                    if random.random() <= subject_prob: # and has_subject:
                        s = random.sample(subject, 1)[0]
                        queryLinePrint = queryLinePrint + " <" + s + "> <" + p + "> ?o ."  # noqa: E501
                        can_q.add((s, p))
                    else:
                        queryLinePrint = queryLinePrint + " ?s" + str(k + 1) + " <" + p + "> ?o ."  # noqa: E501
                        can_q.add((p))

                queryLinePrint = queryLinePrint + "}\n"
                print(queryLinePrint)
                #f.write(queryLinePrint)
                #count = count + 1
                if can_q not in created_queries:
                    # print(queryLinePrint)
                    f.write(queryLinePrint)
                    print(queryLinePrint)
                    created_queries.append(can_q)
                    count = count + 1

    f.close()


if __name__ == '__main__':
    (server, graph, queries, file, subject, n) = get_options()  # noqa: E501

    dataset = ''
    if graph:
        dataset = "FROM " + graph
    generate_star_object(server, queries, file, dataset, subject, n)
    print("Queries are generated!")


####### TERMINAL EXAMPLE: python3 object_star_generator.py -s http://129.13.152.179:8892/sparql -g "<http://localhost/drugbank>" -n 2 -q 1 -f objects_test.rq -sub 0.5  # noqa: E501