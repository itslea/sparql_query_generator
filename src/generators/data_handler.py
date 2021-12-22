import random
import time
import requests


class DataHandler:
    """Handles HTTP requests sent to SPARQL endpoint"""
    def __init__(self):
        self.adress = 'https://dbpedia.org/sparql'  # 'http://localhost:8890/sparql?'
        self.default_graph_uri = 'default-graph-uri='
        self.timeout = str(0)
        self.total_time = 0

    def fetch_data_subject(self, triples):
        """Fetches data from SPARQL endpoint for star-subject-generator"""

        #  Gets subject that fulfills minimum shape criteria
        query = "SELECT DISTINCT ?s FROM <http://dbpedia.org> WHERE {?s ?p1 ?o1. ?s ?p2 ?o2. FILTER(?p1 != ?p2) FILTER(1 > <SHORT_OR_LONG::bif:rnd> (1000, ?s, ?p1, ?o1))} LIMIT 100"
        start_time = time.time()
        result = requests.get(self.adress, params={'format': 'json', 'query': query})
        end_time = time.time()
        needed_time = end_time - start_time
        self.total_time += needed_time

        endpoint_data = result.json()
        s = random.randint(0, 99)
        choosen_subject = endpoint_data['results']['bindings'][s]['s']

        second_query = "SELECT DISTINCT ?p, ?o FROM <http://dbpedia.org> WHERE { <" + choosen_subject['value'] + "> ?p ?o . }"
        second_result = requests.get(self.adress, params={'format': 'json', 'query': second_query})
        second_data = second_result.json()
        pando = second_data['results']['bindings']

        patterns = []
        if len(pando) >= triples:
            choosen_pando = random.choices(pando, k=triples)
            for elem in choosen_pando:
                new_obj = {"s": choosen_subject, "p": elem['p'], "o": elem['o']}
                patterns.append(new_obj)

        return patterns

    def fetch_data_object(self, triples):
        """Fetches data from SPARQL endpoint for star-object-generator"""
        # TODO
        patterns = []
        return patterns

    def fetch_data_path(self, triples):
        """Fetches data from SPARQL endpoint for path-generator"""
        # TODO
        patterns = []
        return patterns

    def get_total_time(self):
        """Gets total time"""
        return str(round(self.total_time, 5))
