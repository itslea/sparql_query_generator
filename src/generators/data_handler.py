import time
import requests


class DataHandler:
    """Handles HTTP requests sent to SPARQL endpoint"""
    def __init__(self):
        self.adress = 'http://localhost:8890/sparql?'
        self.default_graph_uri = 'default-graph-uri='
        self.query = 'query='
        self.format = 'format=json'
        self.timeout = str(0)
        self.signal_void = 'on'
        self.total_time = 0

    def fetch_data(self, query):
        """Fetches data from SPARQL endpoint"""
        self.query += query
        querystring = str(self.adress + self.default_graph_uri + '&' + self.query + '&' + self.format + '&' + self.timeout + '&' + self.signal_void)
        # print(querystring)
        start_time = time.time()
        httprequest = requests.get(querystring)
        end_time = time.time()
        needed_time = end_time - start_time

        self.total_time += needed_time

        result = ""
        for i in httprequest:
            result += i.decode('UTF-8')
        return result

    def get_total_time(self):
        """Gets total time"""
        return str(round(self.total_time, 5))
