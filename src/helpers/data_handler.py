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
        self.limit = 100

    def get_object_string(self, choosen_object):
        object_type = ""
        if choosen_object['type'] == 'uri':
            object_type = '<' + choosen_object['value'] + '>'
        elif choosen_object['type'] == 'literal':
            object_type = '\"' + choosen_object['value'] + '\"' + "@" + choosen_object['xml:lang']
        elif choosen_object['type'] == 'typed-literal':
            if choosen_object['datatype'] == 'http://www.w3.org/2001/XMLSchema#integer':
                object_type = str(choosen_object['value'])
            else:
                object_type = '\"' + choosen_object['value'] + '\"' + "^^<" + choosen_object['datatype'] + ">"

        return object_type

    def fetch_subject(self, triples, choosen_subject, object_is_uri):  # subject = entire json object (incl. type and value)
        second_query = "SELECT DISTINCT ?p, ?o FROM <http://dbpedia.org> WHERE { <" + choosen_subject['value'] + "> ?p ?o . }"
        second_result = requests.get(self.adress, params={'format': 'json', 'query': second_query})
        second_data = second_result.json()
        pando = second_data['results']['bindings']

        patterns = []
        if len(pando) >= triples:
            choosen_pando = random.sample(pando, k=triples)
            for elem in choosen_pando:
                if elem['o']['type'] == "uri" or object_is_uri is False:
                    new_obj = {"s": choosen_subject, "p": elem['p'], "o": elem['o']}
                    patterns.append(new_obj)

        return patterns

    def fetch_object(self, triples, choosen_object):
        object_type = self.get_object_string(choosen_object)
        second_query = "SELECT DISTINCT ?s, ?p FROM <http://dbpedia.org> WHERE {?s ?p " + object_type + " .} LIMIT " + str(self.limit)
        second_result = requests.get(self.adress, params={'format': 'json', 'query': second_query})
        second_data = second_result.json()
        pands = second_data['results']['bindings']
        patterns = []
        if len(pands) >= triples:
            choosen_pands = random.sample(pands, k=triples)
            for elem in choosen_pands:
                new_obj = {"s": elem['s'], "p": elem['p'], "o": choosen_object}
                patterns.append(new_obj)

        return patterns

    def fetch_path(self, triples, choosen_subject):
        patterns = []
        loopcounter = 0
        while loopcounter < triples:
            second_query = "SELECT DISTINCT ?p, ?o FROM <http://dbpedia.org> WHERE { <" + choosen_subject['value'] + "> ?p ?o . ?o ?p1 ?o1 . FILTER(?o != ?o1)} LIMIT " + str(self.limit)
            second_result = requests.get(self.adress, params={'format': 'json', 'query': second_query})
            if second_result.status_code != 200:
                break
            second_data = second_result.json()
            pando = second_data['results']['bindings']
            len_pando = len(pando) - 1
            if len_pando <= 0:
                break
            select_pando_pointer = random.randint(0, len_pando)
            if pando[select_pando_pointer]['o']['type'] == "uri":
                new_obj = {"s": choosen_subject, "p": pando[select_pando_pointer]['p'], "o": pando[select_pando_pointer]['o']}
                patterns.append(new_obj)
                choosen_subject = pando[select_pando_pointer]['o']
                loopcounter = loopcounter + 1

        return patterns

    def fetch_data_subject(self, triples, obj_is_uri):
        """Fetches data from SPARQL endpoint for star-subject-generator"""

        if triples > 100:
            self.limit = triples

        #  Gets subject that fulfills minimum shape criteria
        query = "SELECT DISTINCT ?s FROM <http://dbpedia.org> WHERE {?s ?p1 ?o1. ?s ?p2 ?o2. FILTER(?o1 != ?o2) FILTER(1 > <SHORT_OR_LONG::bif:rnd> (1000, ?s, ?p1, ?o1))} LIMIT " + str(self.limit)
        start_time = time.time()
        result = requests.get(self.adress, params={'format': 'json', 'query': query})
        end_time = time.time()
        needed_time = end_time - start_time
        self.total_time += needed_time

        endpoint_data = result.json()
        s = random.randint(0, self.limit - 1)
        choosen_subject = endpoint_data['results']['bindings'][s]['s']

        return self.fetch_subject(triples, choosen_subject, obj_is_uri)

    def fetch_data_object(self, triples):
        """Fetches data from SPARQL endpoint for star-object-generator"""

        if triples > 100:
            self.limit = triples

        #  Gets object that fulfills minimum shape criteria
        query = "SELECT DISTINCT * FROM <http://dbpedia.org> WHERE {?s1 ?p1 ?o. ?s2 ?p2 ?o. FILTER(?p1 != rdf:type && ?p2 != rdf:type) FILTER(?s1 != ?s2) FILTER(1 > <SHORT_OR_LONG::bif:rnd> (1000, ?s1, ?p1, ?o))} LIMIT " + str(self.limit)
        start_time = time.time()
        result = requests.get(self.adress, params={'format': 'json', 'query': query})
        end_time = time.time()
        needed_time = end_time - start_time
        self.total_time += needed_time

        endpoint_data = result.json()
        o = random.randint(0, self.limit - 1)
        choosen_object = endpoint_data['results']['bindings'][o]['o']

        return self.fetch_object(triples, choosen_object)

    def fetch_data_path(self, triples):
        """Fetches data from SPARQL endpoint for path-generator"""

        if triples > 100:
            self.limit = triples

        query = "SELECT DISTINCT ?s FROM <http://dbpedia.org> WHERE {?s ?p1 ?o. ?o ?p2 ?o2. FILTER(?p1 != ?p2) FILTER(1 > <SHORT_OR_LONG::bif:rnd> (1000, ?s, ?p1, ?o))} LIMIT " + str(self.limit)
        start_time = time.time()
        result = requests.get(self.adress, params={'format': 'json', 'query': query})

        end_time = time.time()
        needed_time = end_time - start_time
        self.total_time += needed_time

        endpoint_data = result.json()
        s = random.randint(0, self.limit - 1)
        choosen_subject = endpoint_data['results']['bindings'][s]['s']

        return self.fetch_path(triples, choosen_subject)

    def fetch_data_mixed(self, triples):  # TODO: muss mind. 4 triple patterns pro query sein
        """Fetches data from SPARQL endpoint for star-subject-generator"""

        if triples > 100:
            self.limit = triples

        choose_shape = ["star_subject", "star_object", "path"]
        first_shape = random.choice(choose_shape)
        choose_shape.remove(str(first_shape))
        second_shape = random.choice(choose_shape)
        first_triples = random.randint(2, triples - 2)
        second_triples = triples - first_triples
        # print(first_triples, second_triples)

        first_patterns = []
        second_patterns = []
        if first_shape == "star_subject":
            if second_shape == "star_object":  # bei path muss object uri sein
                first_patterns = self.fetch_data_subject(first_triples, False)
            elif second_shape == "path":
                first_patterns = self.fetch_data_subject(first_triples, True)
        elif first_shape == "star_object":
            first_patterns = self.fetch_data_object(first_triples)
        elif first_shape == "path":
            first_patterns = self.fetch_data_path(first_triples)

        # print("First-Patterns: ", first_patterns)

        choosen_object = ""
        if first_patterns is not None and len(first_patterns) >= 2:
            choosen_object = random.choice(first_patterns)['o']
            # print("Choosen object: ", choosen_object)
            if second_shape == "star_subject":
                second_patterns = self.fetch_subject(second_triples, choosen_object, False)
            elif second_shape == "star_object":
                second_patterns = self.fetch_object(second_triples, choosen_object)
            elif second_shape == "path":
                second_patterns = self.fetch_path(second_triples, choosen_object)
            # print("Second-Patterns: ", second_patterns)

        print(first_shape, second_shape)
        return {"first": {"shape": first_shape, "patterns": first_patterns}, "second": {"shape": second_shape, "patterns": second_patterns}, "connection": choosen_object}

    def get_total_time(self):
        """Gets total time"""
        return str(round(self.total_time, 5))
