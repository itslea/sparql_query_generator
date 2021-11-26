import random
import requests
import time
import json
from random import randint



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
        print(querystring)
        startTime = time.time()
        httprequest = requests.get(querystring)
        endTime = time.time()
        neededTime = endTime-startTime
        self.totalTime += neededTime
        print(httprequest.text)
        httprequestjson = json.loads(httprequest.text)

        httprequestfilteredjson = httprequestjson['results']['bindings']
        # for i in httprequest:
        #      result += i.decode('UTF-8')
        return httprequestfilteredjson

    def getTotalTime(self):
        return str(round(self.totalTime,5))



    def searchwithsubject(self,s):
        limitValue = randint(5, 10)
        query = ("SELECT distinct  ?p WHERE { " + "<" + str(s) + ">" + " ?p ?o .} LIMIT " + str(limitValue))
        print(query)
        results = self.fetch_data(query)
        #print(results)
        randomUriValue = randint(1,limitValue-1)
        somePredicate = results[randomUriValue]['p'].get('value')
        print(somePredicate)
        return somePredicate

    def searchwithpredicate(self, p):
        limitValue = randint(5, 10)
        query = ("SELECT distinct  ?o WHERE { ?s " + "<" + str(p) + ">" + " ?o .} LIMIT " + str(limitValue))
        print(query)
        results = self.fetch_data(query)
        randomUriValue = randint(1,limitValue-1)
        someObject = results[randomUriValue]['o'].get('value')
        print(someObject)
        return someObject

    def searchwithobject(self, o):
        return

    def searchrandom(self):
        limitValue = randint(5, 10)
        query = "SELECT distinct  ?s WHERE { ?s ?p ?o .} LIMIT " + str(limitValue)
        results = self.fetch_data(query)
        randomUriValue = randint(1,limitValue-1)
        someSubject = results[randomUriValue]['s'].get('value')
        #print(results[randomUriValue]['s'])
        print(someSubject)
        return str(someSubject)
    
        