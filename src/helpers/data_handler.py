import random
import requests


class DataHandler:
    """Handles HTTP requests sent to the SPARQL endpoint and fetches data for triple patterns."""

    def __init__(self, url):
        self.url = url
        self.limit = 100

    def get_object_string(self, choosen_object):
        """Returns corresponding string representation of an object."""

        object_type = ""
        if choosen_object['type'] == 'uri':
            object_type = '<' + choosen_object['value'] + '>'
        elif choosen_object['type'] == 'literal':
            if "\"" in choosen_object['value']:
                choosen_object['value'] = str(choosen_object['value']).replace("\"", "\\\"")
            if 'xml:lang' in choosen_object:
                object_type = "\"" + choosen_object['value'] + "\"" + "@" + choosen_object['xml:lang']
            else:
                object_type = "\"" + choosen_object['value'] + "\""
        elif choosen_object['type'] == 'typed-literal':
            if choosen_object['datatype'] == 'http://www.w3.org/2001/XMLSchema#integer':
                object_type = str(choosen_object['value'])
            else:
                object_type = "\"" + str(choosen_object['value']) + "\"" + "^^<" + str(choosen_object['datatype']) + ">"

        return object_type

    def fetch_subject(self, triples, choosen_subject, object_is_uri):  # subject = entire json object (incl. type and value)
        """Fetches predicates and objects to given subject from the endpoint."""

        if triples > 100:
            self.limit = triples

        query = "SELECT DISTINCT ?p, ?o FROM <http://dbpedia.org> WHERE { <" + choosen_subject['value'] + "> ?p ?o . } LIMIT " + str(self.limit)
        result = requests.get(self.url, params={'format': 'json', 'query': query})
        if result.status_code != 200:
            print(result)
            print(result.reason)
            return []
        second_data = result.json()
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
        """Fetches subjects and predicates to given object from endpoint."""

        if triples > 100:
            self.limit = triples

        object_type = self.get_object_string(choosen_object)
        query = "SELECT DISTINCT ?s, ?p FROM <http://dbpedia.org> WHERE {?s ?p " + object_type + " .} LIMIT " + str(self.limit)
        result = requests.get(self.url, params={'format': 'json', 'query': query})
        if result.status_code != 200:
            print(result)
            print(result.reason)
            return []
        second_data = result.json()
        pands = second_data['results']['bindings']
        patterns = []
        if len(pands) >= triples:
            choosen_pands = random.sample(pands, k=triples)
            for elem in choosen_pands:
                new_obj = {"s": elem['s'], "p": elem['p'], "o": choosen_object}
                patterns.append(new_obj)

        return patterns

    def fetch_path(self, triples, choosen_subject, obj_is_uri):
        """Fetches path structure to given start-subject from endpoint"""

        if triples > 100:
            self.limit = triples

        patterns = []
        loopcounter = 0
        while loopcounter < triples:  # sends as many HTTP requests as needed to fulfill requested number of triple patterns
            query = "SELECT DISTINCT ?p, ?o FROM <http://dbpedia.org> WHERE { <" + choosen_subject['value'] + "> ?p ?o . ?o ?p2 ?o2 . FILTER(?p != <http://xmlns.com/foaf/0.1/primaryTopic>) } LIMIT " + str(self.limit)
            result = requests.get(self.url, params={'format': 'json', 'query': query})
            if result.status_code != 200:
                print(result)
                print(result.reason)
                break
            data = result.json()
            pando = data['results']['bindings']  # pando = p(redicate) and o(bject)
            if len(pando) <= 0:
                break
            pando_uri = []
            for elem in pando:
                if elem['o']['type'] == "uri":
                    pando_uri.append(elem)
            if len(pando_uri) <= 0:  # objects need to be URIs in order to be used as a subject for the next triple pattern
                break
            select_pando_pointer = random.randint(0, len(pando_uri) - 1)
            new_obj = {"s": choosen_subject, "p": pando[select_pando_pointer]['p'], "o": pando[select_pando_pointer]['o']}
            patterns.append(new_obj)
            choosen_subject = pando[select_pando_pointer]['o']
            loopcounter = loopcounter + 1
        if len(patterns) <= 0:
            return []
        pattern_end = self.fetch_path_end(triples, patterns[len(patterns) - 1]['o'], obj_is_uri)  # gets last triple pattern of path
        if len(pattern_end) <= 0:
            return []
        patterns.append(pattern_end)
        return patterns

    def fetch_path_end(self, triples, choosen_subject, obj_is_uri):
        """Fetches path structure to given start-subject from endpoint."""

        if triples > 100:
            self.limit = triples

        new_obj = {}
        query = "SELECT DISTINCT ?p, ?o FROM <http://dbpedia.org> WHERE { <" + choosen_subject['value'] + "> ?p ?o . } LIMIT " + str(self.limit)
        result = requests.get(self.url, params={'format': 'json', 'query': query})
        if result.status_code != 200:
            print(result)
            print(result.reason)
            return []
        data = result.json()
        pando = data['results']['bindings']
        if len(pando) <= 0:
            return []
        if obj_is_uri:  # makes sure objects are URIs
            pando_uri = []
            for elem in pando:
                if elem['o']['type'] == "uri":
                    pando_uri.append(elem)
            if len(pando_uri) <= 0:
                return []
            choose_pando = random.randint(0, len(pando_uri) - 1)
            new_obj = {"s": choosen_subject, "p": pando_uri[choose_pando]['p'], "o": pando_uri[choose_pando]['o']}
            choosen_subject = pando[choose_pando]['o']
        else:
            choose_pando = random.randint(0, len(pando) - 1)
            new_obj = {"s": choosen_subject, "p": pando[choose_pando]['p'], "o": pando[choose_pando]['o']}
            choosen_subject = pando[choose_pando]['o']

        return new_obj

    def fetch_data_subject(self, triples, obj_is_uri):
        """Fetches data from SPARQL endpoint for star-subject-generator."""

        if triples > 100:
            self.limit = triples

        # gets subject that fulfills minimum shape criteria
        query = "SELECT DISTINCT ?s FROM <http://dbpedia.org> WHERE {?s ?p1 ?o1. ?s ?p2 ?o2. FILTER(?o1 != ?o2) FILTER(1 > <SHORT_OR_LONG::bif:rnd> (1000, ?s, ?p1, ?o1))} LIMIT " + str(self.limit)
        result = requests.get(self.url, params={'format': 'json', 'query': query})
        if result.status_code != 200:
            print(result)
            print(result.reason)
            return []
        endpoint_data = result.json()
        s = random.randint(0, self.limit - 1)
        choosen_subject = endpoint_data['results']['bindings'][s]['s']

        return self.fetch_subject(triples, choosen_subject, obj_is_uri)

    def fetch_data_object(self, triples):
        """Fetches data from SPARQL endpoint for star-object-generator."""

        if triples > 100:
            self.limit = triples

        # gets object that fulfills minimum shape criteria
        query = "SELECT DISTINCT * FROM <http://dbpedia.org> WHERE {?s1 ?p1 ?o. ?s2 ?p2 ?o. FILTER(?p1 != rdf:type && ?p2 != rdf:type) FILTER(?s1 != ?s2) FILTER(1 > <SHORT_OR_LONG::bif:rnd> (1000, ?s1, ?p1, ?o))} LIMIT " + str(self.limit)
        result = requests.get(self.url, params={'format': 'json', 'query': query})
        if result.status_code != 200:
            print(result)
            print(result.reason)
            return []
        endpoint_data = result.json()
        o = random.randint(0, self.limit - 1)
        choosen_object = endpoint_data['results']['bindings'][o]['o']

        return self.fetch_object(triples, choosen_object)

    def fetch_data_path(self, triples, obj_is_uri):
        """Fetches data from SPARQL endpoint for path-generator."""

        if triples > 100:
            self.limit = triples

        # gets part of path that fulfills minimum shape criteria
        query = "SELECT DISTINCT ?s FROM <http://dbpedia.org> WHERE {?s ?p1 ?o. ?o ?p2 ?o2. FILTER(?p1 != ?p2) FILTER(1 > <SHORT_OR_LONG::bif:rnd> (1000, ?s, ?p1, ?o)) FILTER(?p1 != <http://xmlns.com/foaf/0.1/primaryTopic>)} LIMIT " + str(self.limit)
        result = requests.get(self.url, params={'format': 'json', 'query': query})
        if result.status_code != 200:
            print(result)
            print(result.reason)
            return []
        endpoint_data = result.json()
        s = random.randint(0, self.limit - 1)
        choosen_subject = endpoint_data['results']['bindings'][s]['s']
        patterns = self.fetch_path(triples, choosen_subject, obj_is_uri)
        if len(patterns) < triples:
            return []

        return patterns

    def fetch_data_mixed(self, triples):  # has to be at least 4 triples otherwise it won't work
        """Fetches data from SPARQL endpoint for star-subject-generator."""

        if triples > 100:
            self.limit = triples

        # decides which shapes to use and their order
        choose_shape = ["star_subject", "star_object", "path"]
        first_shape = random.choice(choose_shape)
        choose_shape.remove(str(first_shape))
        second_shape = random.choice(choose_shape)
        first_triples = random.randint(2, triples - 2)
        second_triples = triples - first_triples

        first_patterns = []
        second_patterns = []
        choosen_object = ""

        # gets data for first shape
        if first_shape == "star_subject":
            if second_shape == "star_object":
                first_patterns = self.fetch_data_subject(first_triples, False)
            elif second_shape == "path":  # last object of star-subject shape has to be an URI
                first_patterns = self.fetch_data_subject(first_triples, True)
            if len(first_patterns) >= 2:
                choosen_object = random.choice(first_patterns)['o']  # choose connecting object for second shape
        elif first_shape == "star_object":
            first_patterns = self.fetch_data_object(first_triples)
            if len(first_patterns) >= 2:
                choosen_object = random.choice(first_patterns)['o']
        elif first_shape == "path":
            first_patterns = self.fetch_data_path(first_triples, True)
            if len(first_patterns) >= 2:
                choosen_object = first_patterns[len(first_patterns) - 1]['o']

        # gets data for second shape
        if len(first_patterns) >= 2:
            if second_shape == "star_subject":
                second_patterns = self.fetch_subject(second_triples, choosen_object, False)
            elif second_shape == "star_object":
                second_patterns = self.fetch_object(second_triples, choosen_object)
            elif second_shape == "path":
                second_patterns = self.fetch_path(second_triples, choosen_object, False)

        print(choosen_object)

        return {"first": {"shape": first_shape, "patterns": first_patterns}, "second": {"shape": second_shape, "patterns": second_patterns}, "connection": choosen_object}
