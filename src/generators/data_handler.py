import requests
import time

class DataHandler:

    def __init__(self):
        self.adress = 'http://localhost:8890/sparql?'
        self.defaultGraphUri = 'default-graph-uri='
        self.query = 'query='
        self.format = 'format=json'
        self.timeout = str(0)
        self.signal_void = 'on'
        self.totalTime = 0
    
    def fetch_data(self, query):
        self.query += query
        querystring = str(self.adress+self.defaultGraphUri+'&'+self.query+'&'+self.format+'&'+self.timeout+'&'+self.signal_void)
        #print(querystring)
        startTime = time.time()
        httprequest = requests.get(querystring)
        endTime = time.time()
        neededTime = endTime-startTime

        self.totalTime += neededTime

        result = ""
        for i in httprequest:
             result += i.decode('UTF-8')
        return result

    def getTotalTime(self):
        return str(round(self.totalTime,5))
        